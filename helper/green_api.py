from whatsapp_api_client_python import API
import os
import json
from dotenv import load_dotenv

from src.generate import process_content

load_dotenv()

greenAPI = API.GreenApi(os.getenv("ID_INSTANCE"), os.getenv("API_TOKEN_INSTANCE"))


def send_message(to: str, message: str):
    result = greenAPI.sending.sendMessage(to, message)
    return result.data


def receive_message():
    greenAPI.webhooks.startReceivingNotifications(onEvent)


def onEvent(typeWebhook, body):
    if typeWebhook == 'incomingMessageReceived':
        onIncomingMessageReceived(body)
    elif typeWebhook == 'deviceInfo':
        onDeviceInfo(body)
    elif typeWebhook == 'incomingCall':
        onIncomingCall(body)
    elif typeWebhook == 'outgoingAPIMessageReceived':
        onOutgoingAPIMessageReceived(body)
    elif typeWebhook == 'outgoingMessageReceived':
        onOutgoingMessageReceived(body)
    elif typeWebhook == 'outgoingMessageStatus':
        onOutgoingMessageStatus(body)
    elif typeWebhook == 'stateInstanceChanged':
        onStateInstanceChanged(body)
    elif typeWebhook == 'statusInstanceChanged':
        onStatusInstanceChanged(body)


def onIncomingMessageReceived(body):
    idMessage = body['idMessage']
    senderData = body['senderData']
    messageData = body['messageData']
    print(idMessage + ': '
          + 'At ' + ' Incoming from ' \
          + json.dumps(senderData, ensure_ascii=False) \
          + ' message = ' + json.dumps(messageData, ensure_ascii=False))
    result = None
    if messageData["typeMessage"] == 'extendedTextMessage':
        result = process_content(messageData["extendedTextMessageData"]["text"], [])
    elif messageData["typeMessage"] == 'textMessage':
        result = process_content(messageData["textMessageData"]["textMessage"], [])

    if result is not None:
        send_message(senderData["sender"], result["answer"])


def onIncomingCall(body):
    idMessage = body['idMessage']
    fromWho = body['from']
    print(idMessage + ': '
          + 'Call from ' + fromWho)


def onDeviceInfo(body):
    deviceData = body['deviceData']
    print('At ' + ': ' \
          + json.dumps(deviceData, ensure_ascii=False))


def onOutgoingMessageReceived(body):
    idMessage = body['idMessage']
    # eventDate = datetime.fromtimestamp(body['timestamp'])
    senderData = body['senderData']
    messageData = body['messageData']
    print(idMessage + ': '
          + 'At ' + ' Outgoing from ' \
          + json.dumps(senderData, ensure_ascii=False) \
          + ' message = ' + json.dumps(messageData, ensure_ascii=False))

    # history = greenAPI.journals.getChatHistory(senderData["chatId"], 20)
    #
    # chat_history = []
    # # if history.code == 200:
    # #     index = 0
    # #     orgHistory = list(reversed(history.data))
    # #     for data in orgHistory:
    # #         if index % 2 == 0:
    # #             tup = (data["textMessage"], history.data[index + 1]["textMessage"])
    # #             chat_history.append(tup)
    # #         index = index + 1
    #
    # # print(chat_history)
    # result = process_content(messageData["extendedTextMessageData"]["text"], chat_history)
    #
    # print(result)
    #
    # send_message(senderData["sender"], result["answer"])


def onOutgoingAPIMessageReceived(body):
    idMessage = body['idMessage']
    senderData = body['senderData']
    messageData = body['messageData']
    print(idMessage + ': '
          + 'At ' + ' API outgoing from ' \
          + json.dumps(senderData, ensure_ascii=False) + \
          ' message = ' + json.dumps(messageData, ensure_ascii=False))


def onOutgoingMessageStatus(body):
    idMessage = body['idMessage']
    status = body['status']
    # eventDate = datetime.fromtimestamp(body['timestamp'])
    print(idMessage + ': '
          + 'At ' + ' status = ' + status)


def onStateInstanceChanged(body):
    stateInstance = body['stateInstance']
    print('At ' + ' state instance = ' \
          + json.dumps(stateInstance, ensure_ascii=False))


def onStatusInstanceChanged(body):
    statusInstance = body['statusInstance']
    print('At ' + ' status instance = ' \
          + json.dumps(statusInstance, ensure_ascii=False))
