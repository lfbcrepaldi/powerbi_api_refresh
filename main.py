'''
Este script atualiza um dataset do power bi via API REST.
'''

import os

import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

load_dotenv()

TENANT_ID = os.environ['AZURE_TENANT_ID']
CLIENT_ID = os.environ['AZURE_CLIENT_ID']
CLIENT_SECRET = os.environ['AZURE_CLIENT_SECRET']

WORKSPACE = os.environ['PBI_WORKSPACE_GESTAO']
REPORT = os.environ['PBI_REPORT_VARIACAO_PDD']

API_URL = 'https://api.powerbi.com/v1.0/myorg'
SCOPE = ['https://analysis.windows.net/powerbi/api/.default']


def obter_token() -> str:
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=f'https://login.microsoftonline.com/{TENANT_ID}',
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if 'access_token' not in result:
        raise RuntimeError(f'Falha na autenticação: {result.get('error_description')}')
    return result['access_token']


def obter_dataset_id(headers: dict, workspace_id: str, report_id: str) -> str:
    r = requests.get(f'{API_URL}/groups/{workspace_id}/reports/{report_id}', headers=headers)
    r.raise_for_status()
    return r.json()['datasetId']


def atualizar_dataset(headers: dict, workspace_id: str, dataset_id: str) -> str:
    r = requests.post(
        f'{API_URL}/groups/{workspace_id}/datasets/{dataset_id}/refreshes',
        headers=headers,
        json={'notifyOption': 'NoNotification'},
    )
    r.raise_for_status()
    return r.headers.get('RequestId', '')


def main():
    descricao = 'Atualização sob demanda'

    headers = {'Authorization': f'Bearer {obter_token()}'}
    dataset_id = obter_dataset_id(headers, WORKSPACE, REPORT)
    request_id = atualizar_dataset(headers, WORKSPACE, dataset_id)

    print(f'{descricao}: iniciada (dataset {dataset_id}, request id {request_id})')


if __name__ == '__main__':
    main()
