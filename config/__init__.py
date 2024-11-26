from flask import Flask
from config.settings import OPENAI_API_KEY, OPENSEARCH_HOST

def create_app():
    app = Flask(__name__)

    # Initialize OpenAI and OpenSearch (if needed)
    app.config['OPENAI_API_KEY'] = OPENAI_API_KEY
    app.config['OPENSEARCH_HOST'] = OPENSEARCH_HOST

    with app.app_context():
        from app.routes import blueprint as routes_blueprint
        app.register_blueprint(routes_blueprint)

    return app