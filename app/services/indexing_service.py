import pandas as pd
from app.services.openai_client import generate_embeddings
from config.settings import OPENSEARCH_INDEX, TEST_CASES_FILE
from utils.opensearch_utils import connect_opensearch, create_index, index_document

def process_test_cases():
    """Reads test cases, calculates embeddings, and indexes them."""
    # Load existing test cases
    test_cases = pd.read_excel(TEST_CASES_FILE)

    required_columns = ["test_case_id", "test_description", "pre_requisite", "test_steps", "expected_result"]
    if not all(col in test_cases.columns for col in required_columns):
        raise ValueError("Missing required columns in the test cases file.")

    client = connect_opensearch()
    create_index(client, OPENSEARCH_INDEX)

    for _, row in test_cases.iterrows():
        embedding_input = " ".join(str(row[col]) for col in required_columns if col != "test_case_id")
        embedding = generate_embeddings(embedding_input)

        document = row.to_dict()
        document["embedding"] = embedding
        index_document(client, document)
