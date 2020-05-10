
ENDPOINTS_CONFIG = {
    'business_units': {
        'path': 'business_units_structure',
        'auth': 'app',
        'paginate': False,
        'data_key': 'business_units',
        'replication_method': 'incremental',
        'replication_field': 'updated_at',
        'pk': ['id']
    },
    'projects': {
        'path': 'projects',
        'auth': 'app',
        'params': {
            'sort': '-updated_at'
        },
        'replication_method': 'incremental',
        'replication_field': 'updated_at',
        'pk': ['id']
    }
}
