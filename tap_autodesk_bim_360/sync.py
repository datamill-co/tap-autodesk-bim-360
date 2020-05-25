import singer
from singer import metrics, metadata, Transformer
from singer.bookmarks import set_currently_syncing

from tap_autodesk_bim_360.discover import discover
from tap_autodesk_bim_360.endpoints import ENDPOINTS_CONFIG

LOGGER = singer.get_logger()

def nested_get(dic, path):
    for key in path:
        value = dic.get(key)
        if value is None or key == path[-1]:
            return value
        dic = value

def get_bookmark(state, stream_name, default):
    return state.get('bookmarks', {}).get(stream_name, default)

def write_bookmark(state, stream_name, value):
    if 'bookmarks' not in state:
        state['bookmarks'] = {}
    state['bookmarks'][stream_name] = value
    singer.write_state(state)

def write_schema(stream):
    schema = stream.schema.to_dict()
    singer.write_schema(stream.tap_stream_id, schema, stream.key_properties)

def sync_endpoint(client,
                  catalog,
                  state,
                  required_streams,
                  selected_streams,
                  stream_name,
                  endpoint,
                  key_bag):
    persist = endpoint.get('persist', True)
    url = None

    if persist:
        stream = catalog.get_stream(stream_name)
        schema = stream.schema.to_dict()
        mdata = metadata.to_map(stream.metadata)
        write_schema(stream)

    if 'url' in endpoint:
        url = endpoint['url'].format(**key_bag)

    LOGGER.info('{} - Syncing: {}'.format(
                stream_name,
                url))

    limit = 100
    offset = 0
    while True:
        params = endpoint.get('params', {})

        if endpoint.get('paginate', True):
            params[endpoint['paginate_limit_param']] = limit
            params[endpoint['paginate_offset_param']] = offset

            LOGGER.info('{} - {} - limit: {}, offset: {}'.format(
                stream_name,
                url,
                limit,
                offset))

        data = client.request('GET',
                              url=url,
                              params=params,
                              auth=endpoint.get('auth'),
                              endpoint=stream_name,
                              ignore_http_status_codes=endpoint.get('ignore_http_status_codes', []))

        if data is None:
            return

        if 'data_key' in endpoint:
            records = data[endpoint['data_key']]
        elif isinstance(data, list):
            records = data
        else:
            records = [data]

        with metrics.record_counter(stream_name) as counter:
            with Transformer() as transformer:
                for record in records:
                    if persist and stream_name in selected_streams:
                        record = {**record, **key_bag}
                        record_typed = transformer.transform(record,
                                                             schema,
                                                             mdata)
                        singer.write_record(stream_name, record_typed)
                        counter.increment()
                    if 'children' in endpoint:
                        child_key_bag = dict(key_bag)

                        if 'provides' in endpoint:
                            for dest_key, obj_path in endpoint['provides'].items():
                                if not isinstance(obj_path, list):
                                    obj_path = [obj_path]
                                child_key_bag[dest_key] = nested_get(record, obj_path)

                        for child_stream_name, child_endpoint in endpoint['children'].items():
                            if child_stream_name in required_streams:
                                sync_endpoint(client,
                                              catalog,
                                              state,
                                              required_streams,
                                              selected_streams,
                                              child_stream_name,
                                              child_endpoint,
                                              child_key_bag)

        if endpoint.get('paginate', True) and len(records) == limit:
            if endpoint.get('paginate_units') == 'pages':
                offset += 1
            else:
                offset += limit
        else:
            break

def update_current_stream(state, stream_name=None):  
    set_currently_syncing(state, stream_name) 
    singer.write_state(state)

def get_required_streams(endpoints, selected_stream_names):
    required_streams = []
    for name, endpoint in endpoints.items():
        child_required_streams = None
        if 'children' in endpoint:
            child_required_streams = get_required_streams(endpoint['children'],
                                                          selected_stream_names)
        if name in selected_stream_names or child_required_streams:
            required_streams.append(name)
            if child_required_streams:
                required_streams += child_required_streams
    return required_streams

def sync(client, config, catalog, state):
    if not catalog:
        catalog = discover()
        selected_streams = catalog.streams
    else:
        selected_streams = catalog.get_selected_streams(state)

    selected_stream_names = []
    for selected_stream in selected_streams:
        selected_stream_names.append(selected_stream.tap_stream_id)

    required_streams = get_required_streams(ENDPOINTS_CONFIG, selected_stream_names)

    key_bag = {
        'account_id': config['account_id']
    }

    for stream_name, endpoint in ENDPOINTS_CONFIG.items():
        if stream_name in required_streams:
            update_current_stream(state, stream_name)
            sync_endpoint(client,
                          catalog,
                          state,
                          required_streams,
                          selected_stream_names,
                          stream_name,
                          endpoint,
                          key_bag)

    update_current_stream(state)
