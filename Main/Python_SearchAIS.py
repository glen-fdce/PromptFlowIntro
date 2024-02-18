from promptflow import tool
from promptflow.connections import CognitiveSearchConnection
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential


@tool
def searchAzureAI(ais: CognitiveSearchConnection, indexName: str, searchQueryText: str, maxResults: int, searchQueryEmbeddings: list[float]) -> list[dict[str, str]]:

    searchClient = SearchClient(
        endpoint = ais.api_base,
        index_name = indexName,
        credential = AzureKeyCredential(ais.api_key)
    )

    selectParams=["FileName", "Text"]

    searchParams = {
        "search_text": searchQueryText,
        "select": selectParams
    }

    if maxResults > 0:
        searchParams["top"] = maxResults

    if(searchQueryEmbeddings):
        vectorQuery = VectorizedQuery(vector=searchQueryEmbeddings, k_nearest_neighbors=100, fields="Embedding")
        searchParams = {**searchParams, **{"vector_queries": [vectorQuery]}}

    results = searchClient.search(**searchParams)

    docs = [{"FileName": doc["FileName"], "Text": doc["Text"]} for doc in results]

    return docs
