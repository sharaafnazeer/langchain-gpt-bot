from flask import Flask, request, jsonify
from helper.pinecone_api import create_index
from helper.green_api import send_message
from src.generate import generate_content, process_content
app = Flask(__name__)


@app.route('/')
def home():
    return jsonify(
        {
            'status': 'OK',
            'wehook_url': 'BASEURL/recieve',
            'message': 'The webhook is ready.',
        }
    )


@app.route('/create-index', methods=['GET'])
def generate():
    create_index()
    return 'OK', 200


@app.route('/generate', methods=['GET'])
def generate_vectors():
    generate_content()
    return jsonify(
        {
            'status': 'OK',
            'message': 'Vectors generated successfully.',
        }
    ), 200

@app.route('/recieve', methods=['GET'])
def receiveMessage():
    try:
        # Extract incomng parameters from Twilio
        # message = request.form['Body']
        # sender_id = request.form['From']

        result = process_content('what is the employee name', [])

        print(result)

        send_message("94779592868@c.us", result["answer"])

        return jsonify(
            {
                'status': 'OK',
                'message': result["answer"],

            }
        ), 400
    except Exception as err:
        print(err)
        return jsonify(
            {
                'status': 'Failed',
                'message': "",

            }
        ), 400