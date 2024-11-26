from plaid import Configuration, ApiClient, Environment
from django.conf import settings
from plaid.api import plaid_api


# Configure Plaid API client with SSL verification disabled
configuration = Configuration(
    host=Environment.Sandbox,
    api_key={
        'clientId': settings.PLAID_CLIENT_ID,
        'secret': settings.PLAID_SECRET,
    },
    verify_ssl=False  # Disable SSL verification (ONLY for development purposes)
)
api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)


