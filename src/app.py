from flask import Flask, request, jsonify, session
from helper.pinecone_api import create_index, delete_index
from helper.green_api import send_message, receive_message
from src.generate import generate_content, process_content, test
import json

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(
        {
            'status': 'OK',
            'message': 'The api is ready.',
        }
    )


@app.route('/create-index', methods=['GET'])
def generate():
    create_index()
    return 'OK', 200


@app.route('/generate', methods=['GET'])
def generate_vectors():
    try:
        delete_index()
        create_index()
        generate_content()

    except Exception as err:
        print(err)
        return jsonify(
            {
                'status': 'Failed',
                'message': 'Vectors not generated successfully.',
            }
        ), 200

    return jsonify(
        {
            'status': 'OK',
            'message': 'Vectors generated successfully.',
        }
    ), 200


@app.route('/chat', methods=['POST'])
def receive_message():
    try:

        dict_str = request.data.decode("UTF-8")
        data = json.loads(dict_str)

        chat_history = []
        if session.get("chat_history") is not None:
            if type(session.get('chat_history')) != str:
                chat_history = session.get('chat_history')
        result = process_content(data["question"], chat_history)

        if session.get('chat_history') is not None:
            session['chat_history'].append((data["question"], result["answer"]))
            session.modified = True
        else:
            session['chat_history'] = [(data["question"], result["answer"])]

        return jsonify(
            {
                'status': 'OK',
                'result': {
                    'answer': result["answer"],
                    'chat_history': session.get('chat_history')
                }

            }
        ), 200
    except Exception as err:
        print(err)
        return jsonify(
            {
                'status': 'Failed',
                'message': "Something went wrong",

            }
        ), 400


@app.route('/receive', methods=['POST'])  # not being used, delay
def chat_message():
    try:

        dict_str = request.data.decode("UTF-8")
        data = json.loads(dict_str)

        print(data)
        chat_history = []
        if session.get("chat_history") is not None:
            if type(session.get('chat_history')) != str:
                chat_history = session.get('chat_history')
        result = None
        message = ''
        if data["typeWebhook"] == "incomingMessageReceived":
            if data["messageData"]["typeMessage"] == 'extendedTextMessage':
                message = data["messageData"]["extendedTextMessageData"]["text"]
                result = process_content(message, chat_history)
            elif data["messageData"]["typeMessage"] == 'textMessage':
                message = data["messageData"]["textMessageData"]["textMessage"]
                result = process_content(message, chat_history)

        if result is not None:
            send_message(data["senderData"]["sender"], result["answer"])
            if session.get('chat_history') is not None:
                session['chat_history'].append((message, result["answer"]))
                session.modified = True
            else:
                session['chat_history'] = [(message, result["answer"])]

        return jsonify(
            {
                'status': 'OK',
            }
        ), 200
    except Exception as err:
        print(err)
        return jsonify(
            {
                'status': 'Failed',
                'message': "Something went wrong",

            }
        ), 400


@app.route('/clear', methods=['GET'])
def clear_session():
    session.clear()
    return jsonify(
        {
            'status': 'OK',
            'message': 'Session cleared successfully.',
        }
    ), 200


@app.route('/test', methods=['GET'])
def testing():
    test()
