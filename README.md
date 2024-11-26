# **AIRA - AI Regression Advisor**

AIRA (**AI Regression Advisor**) is an AI-powered tool designed to enhance and streamline regression testing processes. With AIRA, you can efficiently search for test cases, generate new test cases using AI, and receive actionable testing insights to optimize your test strategy.

## Demo

![AIRA Demo](assets/aira-demo.gif)

## **Features**
- **KNN-Based Test Case Retrieval**:
  - Quickly retrieve relevant test cases using a K-Nearest Neighbors (KNN) query based on semantic similarity to user input.
- **AI-Generated Test Cases**:
  - Generate additional, unique test cases with GPT to complement existing ones.
- **Test Focus Insights**:
  - Receive a concise summary of critical testing areas based on both retrieved and AI-generated test cases.
- **Scheduled Job**:
  - Automatically refreshes test cases from your Excel file daily, calculates embeddings, and updates the OpenSearch index.
- **Modern UI**:
  - Intuitive and responsive interface to search and expose test cases.
- **Differentiation of Results**:
  - OpenSearch-derived test cases and AI-generated ones are clearly marked and separated for easy identification.

---

## **Setup and Installation**

### **1. Prerequisites**
- Python 3.8 or higher
- Docker (for running OpenSearch)
- An OpenAI API Key (for GPT-based features)

### **2. Clone the Repository**
```bash
git clone <repository-url>
cd aira
```

### **3. Install Dependencies**
Create a virtual environment and install the required Python packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### **4. Start OpenSearch**
Run OpenSearch in a Docker container:

```bash
docker run -p 9200:9200 -p 9600:9600 \
  --name opensearch \
  --env "discovery.type=single-node" \
  --env "OPENSEARCH_INITIAL_ADMIN_PASSWORD=YourStrongPassword123" \
  opensearchproject/opensearch:latest
```

### **5. Configure OpenAI API Key**
Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your-openai-api-key"  # On Windows, use `set`
```

Alternatively, update the `OPENAI_API_KEY` in the `config/settings.py` file.

### **6. Run the Application**
Start the Flask app:
```bash
python main.py
```

Visit the app in your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## **Daily Scheduled Service**

AIRA includes a scheduled service that refreshes test cases on a daily schedule. The job:
1. Reads the **test_cases.xlsx** file from the `data/` directory.
2. Calculates new embeddings for each test case using OpenAI's embedding model.
3. Updates the OpenSearch index with the refreshed test cases and their embeddings.

### **How It Works**
- The service runs every 24 hours using **APScheduler**.
- The scheduled job triggers the `/trigger` API endpoint, which:
  - Processes test cases from the Excel file.
  - Generates embeddings for the descriptions.
  - Updates the OpenSearch index.

### **Customizing the Schedule**
You can adjust the schedule interval in `app/scheduler.py`:
```python
scheduler.add_job(
    lambda: app.test_client().post('/trigger'),
    'interval',
    seconds=86400  # Runs every 24 hours
)
```

To change the interval:
- **For hourly execution**: Set `seconds=3600`.
- **For weekly execution**: Set `seconds=604800`.

---

## **Usage**

### **Search for Test Cases**
1. Enter a feature query (e.g., "Verify checkout process for anonymous users").
2. Optionally, enable **"Include extra suggestions"** to generate additional test cases using AI.

### **Explore Results**
- View OpenSearch-derived test cases and AI-generated test cases in a structured table.
- Each test case includes:
  - **Test Case ID**
  - **Description**
  - **Pre-requisite**
  - **Steps**
  - **Expected Result**

### **Test Focus**
- View the **Test Focus** section for actionable insights summarizing the most critical areas of testing based on your query.

---

## **Project Structure**
```
aira/
│
├── app/
│   ├── __init__.py             # Initializes the Flask app
│   ├── routes.py               # Defines Flask routes for the UI and API
│   ├── scheduler.py            # Manages the daily scheduled job
│   ├── services/
│   │   ├── openai_client.py    # Generates embeddings using OpenAI
│   │   ├── indexing_service.py # Manages OpenSearch indexing
│   │   └── query_service.py    # Handles OpenSearch KNN queries
│   ├── templates/
│   │   └── index.html          # Frontend HTML for the UI
│   └── static/
│       └── style.css           # CSS for styling the UI
│                               # JavaScript for dynamic UI elements
│
├── config/
│   ├── __init__.py             # Configuration initialization
│   └── settings.py             # Configuration settings (e.g., API keys)
│
├── utils/
│   ├── opensearch_utils.py     # OpenSearch utils
│
├── data/                       # Directory for storing test case data
│   └── test_cases.xlsx         # Sample test case data (replaceable)
│
├── main.py                     # Entry point to start the Flask app
├── requirements.txt            # List of Python dependencies
└── README.md                   # Documentation for the project
```

---

## **Technical Details**

### **1. OpenSearch Integration**
- Test cases are indexed in OpenSearch with vector embeddings for semantic similarity searches.
- **KNN Query**: Uses OpenSearch’s dense vector capabilities to retrieve relevant test cases.

### **2. OpenAI Integration**
- Generates embeddings for feature queries and test case descriptions.
- Creates new test cases and summarizes key testing areas via GPT.

### **3. Scheduled Service**
- Automatically refreshes test cases daily by processing the `test_cases.xlsx` file, updating the embeddings, and re-indexing the test cases.

---

## **Customizations**

1. **Update Minimum Similarity Threshold**
   - Modify the `min_score` parameter in `knn_query` to adjust the relevance of retrieved test cases.

2. **Customize AI Behavior**
   - Update the prompt in `openai_client.py` to refine test case generation or focus summaries.

3. **Change Scheduling Interval**
   - Edit the `seconds` parameter in the `scheduler.add_job` configuration.

---

## **Future Enhancements**
- Integration with CI/CD pipelines for automated regression testing.
- Support for multiple languages in test case descriptions.

---

## **Contributing**

We welcome contributions to improve AIRA! Feel free to:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with detailed changes.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Acknowledgments**

- OpenAI for powering the AI-driven test case generation.
- OpenSearch for efficient semantic similarity-based retrieval.

---
