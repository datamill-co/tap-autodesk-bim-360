
ENDPOINTS_CONFIG = {
    'business_units': {
        'url': 'https://developer.api.autodesk.com/hq/v1/accounts/{account_id}/business_units_structure',
        'auth': 'app',
        'paginate': False,
        'data_key': 'business_units',
        'replication_method': 'incremental',
        'replication_field': 'updated_at',
        'pk': ['id']
    },
    'projects': {
        'url': 'https://developer.api.autodesk.com/hq/v1/accounts/{account_id}/projects',
        'auth': 'app',
        'params': {
            'sort': '-updated_at'
        },
        'replication_method': 'incremental',
        'replication_field': 'updated_at',
        'pk': ['id'],
        'paginate_limit_param': 'limit',
        'paginate_offset_param': 'offset'
    },
    'hub_projects': {
        'persist': False,
        'url': 'https://developer.api.autodesk.com/project/v1/hubs/b.{account_id}/projects',
        'auth': 'app',
        'data_key': 'data',
        'paginate_limit_param': 'page[limit]',
        'paginate_offset_param': 'page[number]',
        'paginate_units': 'pages',
        'provides': {
            'project_id': 'id',
            'container_id': ['relationships', 'checklists', 'data', 'id'],
            'root_folder_id': ['relationships', 'rootFolder', 'data', 'id']
        },
        'children': {
            'checklists': {
                'url': 'https://developer.api.autodesk.com/bim360/checklists/v1/containers/{container_id}/instances',
                'auth': 'user',
                'pk': ['id'],
                'data_key': 'data',
                'paginate_limit_param': 'page[limit]',
                'paginate_offset_param': 'page[offset]',
                'ignore_http_status_codes': [403]
            },
            'issues': {
                'url': 'https://developer.api.autodesk.com/issues/v1/containers/{container_id}/quality-issues',
                'auth': 'user',
                'pk': ['id'],
                'data_key': 'data',
                'paginate_limit_param': 'page[limit]',
                'paginate_offset_param': 'page[offset]',
                'ignore_http_status_codes': [401, 403]
            },
            'folder_contents': {
                'url': 'https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{root_folder_id}/contents',
                'auth': 'user',
                'pk': ['id'],
                'data_key': 'data',
                'paginate_limit_param': 'page[limit]',
                'paginate_offset_param': 'page[number]',
                'paginate_units': 'pages',
                'ignore_http_status_codes': [403]
            }
        }
    }
}
