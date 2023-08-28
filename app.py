import json
import subprocess
import sys
import time
import requests
import websocket
import os


SUBSCRIBED_TOPICS = [
    "SIFIS:Privacy_Aware_Speech_Recognition_Results",
]

DHT_ADDRESS = "localhost:3000"

def turn(ws, topic_name, topic_uuid, on):

    command = {
        "timestamp": time.time(),
        "command": {
            "command_type": "turn_command",
            "value": {
                "topic_name": topic_name,
                "topic_uuid": topic_uuid,
                "desired_state": on
            }
        }
    }

    ws_req = {
        "RequestPubMessage":
            {
                "value": command
             }
    }

    ws.send(json.dumps(ws_req))

def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")


def on_open(ws):
    print("### Connection established ###")


def on_message(ws, message):
    json_message = json.loads(message)

    if "Persistent" in json_message:
        json_message = json_message["Persistent"]

        if "topic_name" in json_message:
            if json_message["topic_name"] in SUBSCRIBED_TOPICS:
                if (
                    json_message["topic_name"]
                    == "SIFIS:Privacy_Aware_Speech_Recognition_Results"
                ):
                    print("Received instance of " + json_message["topic_name"])
                    print(
                        "Private_Text: "
                        + json_message["value"]["Private_Text"]
                    )

                    Private_Text = json_message["value"]["Private_Text"]
                    requestor_id = json_message["value"]["requestor_id"]
                    request_id = json_message["value"]["request_id"]
                    print("You said: ", Private_Text)
    
                    if Private_Text.lower() != "" and "turn on" in Private_Text.lower() and "light" in Private_Text.lower():
                        print("Turn on")
                        turn(ws, "domo_light",  "3812729d-a8fd-4d44-a820-8ab32759f0f7", True)

                        ws_req = {
                                "RequestPostTopicUUID": {
                                    "topic_name": "SIFIS:notification_message",
                                    "topic_uuid": "notification_message_uuid",
                                    "value": {
                                        "message": "Light turned on",
                                        "requestor_id": str(requestor_id),
                                        "request_id": str(request_id),
                                    },
                                }
                            }
                        ws.send(json.dumps(ws_req))

                    if Private_Text.lower() != "" and "turn off" in Private_Text.lower() and "light" in Private_Text.lower():
                        print("Turn off")
                        turn(ws, "domo_light",  "3812729d-a8fd-4d44-a820-8ab32759f0f7", False)
                        ws_req = {
                                "RequestPostTopicUUID": {
                                    "topic_name": "SIFIS:notification_message",
                                    "topic_uuid": "notification_message_uuid",
                                    "value": {
                                        "message": "Light turned off",
                                        "requestor_id": str(requestor_id),
                                        "request_id": str(request_id),
                                    },
                                }
                            }
                        ws.send(json.dumps(ws_req))

                    else:
                        print("Unkown command")
                    
            else:
                print(
                    "We are not subscribed to this topic ",
                    json_message["topic_name"],
                )


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "ws://localhost:3000/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()
