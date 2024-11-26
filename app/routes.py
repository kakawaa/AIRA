from flask import Blueprint, request, render_template, jsonify
from app.services.indexing_service import process_test_cases
from app.services.openai_client import get_chatgpt_suggestions_with_context
from app.services.query_service import query_knn, query_by_field

blueprint = Blueprint("routes", __name__)

@blueprint.route('/trigger', methods=['POST'])
def trigger_job():
    """API endpoint to manually trigger the test case processing job."""
    process_test_cases()
    return jsonify({"status": "success", "message": "Test cases processed and indexed."})

@blueprint.route('/', methods=['GET', 'POST'])
def knn_ui():
    """UI for users to query relevant test cases."""
    if request.method == 'POST':
        query_text = request.form['query']
        use_chatgpt = 'use_chatgpt' in request.form

        knn_results = query_knn(query_text, k=5)

        # OpenSearch results
        open_search_results = [
            {
                "test_case_id": hit["_source"]["test_case_id"],
                "test_description": hit["_source"]["test_description"],
                "pre_requisite": hit["_source"]["pre_requisite"],
                "test_steps": hit["_source"]["test_steps"],
                "expected_result": hit["_source"]["expected_result"]
            }
            for hit in knn_results["hits"]["hits"]
        ]

        # ChatGPT suggestions and summary
        chatgpt_suggestions = []
        focused_summary = "No summary available."
        if use_chatgpt:
            chatgpt_suggestions, focused_summary = get_chatgpt_suggestions_with_context(query_text, open_search_results)

        return render_template(
            'index.html',
            open_search_results=open_search_results,
            chatgpt_suggestions=chatgpt_suggestions,
            focused_summary=focused_summary
        )

    return render_template('index.html', open_search_results=[], chatgpt_suggestions=[], focused_summary="No summary available.")

@blueprint.route('/query', methods=['GET'])
def query_test_case():
    """API endpoint for querying test cases by field."""
    field = request.args.get("field")
    value = request.args.get("value")
    results = query_by_field(field, value)
    return jsonify(results)


