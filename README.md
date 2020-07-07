# tap-autodesk-bim-360

This is a [Singer](https://www.singer.io/) tap that produces JSON-formatted data following the Singer spec.

See the getting [started guide for running taps.](https://github.com/singer-io/getting-started/blob/master/docs/RUNNING_AND_DEVELOPING.md#running-singer-with-python)

This tap:

- Pulls raw data from the Autodesk Forge [BIM 360 API](https://forge.autodesk.com/en/docs/bim360/v1/reference/http/) and [Data Management API](https://forge.autodesk.com/en/docs/data/v2/reference/http/).
- Extracts the following resources:
  - [business_units](https://forge.autodesk.com/en/docs/bim360/v1/reference/http/business_units_structure-GET/)
  - [projects](https://forge.autodesk.com/en/docs/bim360/v1/reference/http/projects-GET/)
  - [checklists](https://forge.autodesk.com/en/docs/bim360/v1/reference/http/checklists-instances-GET/)
  - [issues](https://forge.autodesk.com/en/docs/bim360/v1/reference/http/field-issues-GET/)
  - [folder_contents](https://forge.autodesk.com/en/docs/data/v2/reference/http/projects-project_id-folders-folder_id-contents-GET/) - Project root folder contents

### Authentication

The tap needs to be [associated with an app](https://forge.autodesk.com/en/docs/oauth/v2/tutorials/create-app/).

The tap uses two forms of authentication:
- OAuth `client_credentials` for endpoints that use the "app" authentication context.
- OAuth `refresh_token` for endpoints that use the "user" authentication context.

A separate access token is generated and tracked for each form of OAuth during each run.

For the "app" authentication endpoints to work, the app whose credentials are added to the config file must be added to the BIM 360 account.

For the "user" authentication endpoints to work, the user must have access to those resource. Resrouces are also on a per project basis. Checklists, issues, and folder_contents will be replicated if access is allowed (a 403 is not received).

### Config File

```json
{
  "start_date": "2000-01-01T00:00:00Z",
  "account_id": <ACCOUNT_ID>,
  "client_id": <CLIENT_ID>,
  "client_secret": <CLIENT_SECRET>,
  "refresh_token": <REFRESH_TOKEN>
}
```

---

Copyright &copy; 2020 Data Mill Services, LLC
