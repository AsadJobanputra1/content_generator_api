from flask import Flask, request, jsonify
import openai
from content_generator import generate_article
from feedback_analyzer import analyze_article
from content_editor import edit_article
from get_markdown import getmarkdown_article
import os
from dotenv import load_dotenv
from flask_cors import CORS
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app, 
     resources={r"/*": {"origins": "*"}}, 
)

@app.route('/version', methods=['GET','POST'])
def test_endpoint():
    print(f"recieved request /version")
    response = jsonify({"version":"0.1"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
    return response
@app.route('/generate_article', methods=['POST'])
def generate_article_endpoint():
    print(f"recieved request /generate_article")
    data = request.json
    article = generate_article(topic=data.get('topic', ''), # type: ignore
                               target_audience=data.get('target_audience', ''), # type: ignore
                               audience_questions=data.get('audience_questions', ''), # type: ignore
                               purpose=data.get('purpose', ''), # type: ignore
                               detail_info=data.get('detail_info', ''), # type: ignore
                               length=data.get('length', '500 words'), # type: ignore
                               style=data.get('style', 'informative')) # type: ignore
    response = jsonify(article)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
    return response


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# This will log to a file called 'flask.log'
file_handler = logging.FileHandler('flask.log')
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

@app.route('/provide_feedback', methods=['POST'])
def provide_feedback_endpoint():
    data = request.json
    feedback = analyze_article(article=data.get('article', ''), # type: ignore
                               persona=data.get('persona', ''),# type: ignore
                               job_description=data.get('job_description', ''))# type: ignore
    return jsonify(feedback)


@app.route('/edit_article', methods=['POST'])
def edit_article_endpoint():
    data = request.json
    edited_article = edit_article(article=data.get('article', ''),
                                  guidance=data.get('guidance', '')
                                  )
    return jsonify(edited_article)

@app.route('/getmarkdown_article', methods=['POST'])
def getmarkdown_article_endpoint():
    data = request.json
    response = getmarkdown_article(article=data.get('article', '')
                                  )
    return jsonify(response)


if __name__ == '__main__':
    # Get the host and port from the environment variables, with defaults
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False') == 'True'

    # Run the Flask app with the configuration from the .env file
    app.run(host=host, port=port, debug=debug)