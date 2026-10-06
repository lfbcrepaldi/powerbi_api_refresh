# powerbi_api_refresh

Dispara sob demanda a atualização de um dataset do Power BI pela API REST, autenticando com um service principal do Azure (MSAL).

## Requisitos

- Python 3.12+
- App registrado no Azure AD com acesso ao workspace do Power BI

## Uso

```bash
pip install -r requirements.txt
cp .env.example .env   # preencha tenant, client, secret, workspace e report
python main.py
```

O script busca o dataset vinculado ao relatório e inicia o refresh, imprimindo o request id retornado pela API.
