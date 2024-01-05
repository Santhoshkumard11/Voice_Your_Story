import requests
import json


def send_request(method="get", endpoint="", payload=None):
    response = ""
    if method == "get":
        response = requests.get(endpoint)

    if method == "post":
        if payload is None:
            raise Exception("Payload can't be empty for this post request")
        response = requests.post(endpoint, payload)

    return response


def format_llm_output(response):
    for char_ in ["\n", "'", "```json", "```"]:
        response = response.replace(char_, "")

    response = json.loads(response)

    return response
