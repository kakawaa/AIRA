import os

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")

# OpenSearch Configuration
OPENSEARCH_HOST = "http://localhost:9200"
OPENSEARCH_INDEX = "test_cases"

# File Paths
TEST_CASES_FILE = os.path.join(os.path.dirname(__file__), "../data/test_cases.xlsx")

# Scheduler Configuration
SCHEDULE_INTERVAL = 86400  # 24 hours in seconds