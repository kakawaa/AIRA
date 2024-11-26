from utils.opensearch_utils import knn_search, field_search

def query_knn(query_text, k=5):
    """Perform a KNN query to retrieve similar test cases."""
    from app.services.openai_client import generate_embeddings
    query_vector = generate_embeddings(query_text)
    return knn_search(query_vector, k)

def query_by_field(field, value):
    """Perform a field-based search."""
    return field_search(field, value)
