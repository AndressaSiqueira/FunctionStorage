import logging
import azure.functions as func
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Testando conexão com Blob Storage via Managed Identity")

    try:
        storage_account_name = "testeid89f8"  # sem .blob.core.windows.net
        container_name = "codigo"

        account_url = f"https://{storage_account_name}.blob.core.windows.net"
        credential = ManagedIdentityCredential()

        blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
        container_client = blob_service_client.get_container_client(container_name)

        blobs = container_client.list_blobs()
        blob_names = [blob.name for blob in blobs]

        return func.HttpResponse(
            f"Conexão bem-sucedida. Blobs encontrados:\n" + "\n".join(blob_names),
            status_code=200
        )

    except Exception as e:
        logging.error(f"Erro ao acessar Blob Storage: {e}")
        return func.HttpResponse(
            f"Erro ao acessar Blob Storage: {str(e)}",
            status_code=500
        )
