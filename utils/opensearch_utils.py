from opensearchpy import OpenSearch
from config.settings import OPENSEARCH_HOST, OPENSEARCH_INDEX

def connect_opensearch():
    """Connect to OpenSearch."""
    return OpenSearch(
        hosts=[OPENSEARCH_HOST],
        http_auth=("admin", "InsertAdminPasswordHere")  # Adjust credentials as needed
    )

def create_index(client, index_name):
    """Create an OpenSearch index with knn_vector mapping."""
    mapping = {
        "settings": {
            "index": {
                "knn": True  # Enable KNN on the index
            }
        },
        "mappings": {
            "properties": {
                "test_case_id": {"type": "keyword"},
                "module_id": {"type": "keyword"},
                "test_description": {"type": "text"},
                "pre_requisite": {"type": "text"},
                "test_steps": {"type": "text"},
                "expected_result": {"type": "text"},
                "actual_result": {"type": "text"},
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 1536  # Set the dimension size of the vector
                }
            }
        }
    }

    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name, body=mapping)
        print(f"Created index: {index_name}")
    else:
        print(f"Index already exists: {index_name}")


def index_document(client, document):
    """Index a document in OpenSearch."""
    document_id = document["test_case_id"]
    client.index(index=OPENSEARCH_INDEX, id=document_id, body=document)

def knn_search(query_vector, k=5):
    """Perform a KNN search in OpenSearch."""
    body = {
        "size": k,
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_vector,
                    "k": k
                }
            }
        },
        "_source": ["test_case_id", "test_description", "pre_requisite", "test_steps", "expected_result"],  # Return only necessary fields
        "min_score": 0.7
    }
    return connect_opensearch().search(index=OPENSEARCH_INDEX, body=body)

def field_search(field, value):
    """Perform a field-based search in OpenSearch."""
    body = {
        "query": {
            "term": {
                field: {"value": value}
            }
        }
    }
    return connect_opensearch().search(index=OPENSEARCH_INDEX, body=body)
