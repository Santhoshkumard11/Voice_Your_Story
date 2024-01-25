import logging
import os
import requests
import json
from .constants import STORY3_API_ENDPOINTS

STORY3_API_KEY = os.getenv("STORY3_API_KEY")


def format_twists_text(twist_data):
    formatted_dict = {}

    # Accessing and printing twist text with keys in order
    twist_texts_with_keys = get_twist_text_with_key(twist_data, "")
    for key, twist_text in twist_texts_with_keys:
        key = key.split("#")[-1].split("-")[-1]
        formatted_dict.update({key: twist_text})

    return formatted_dict


def get_twist_text_with_key(data, key_prefix="", order=None):
    if order is None:
        order = []

    if isinstance(data, list):
        for i, item in enumerate(data, start=1):
            if isinstance(item, str):
                order.append((f"{key_prefix}", item))
            else:
                order.extend(get_twist_text_with_key(item, f"{key_prefix}#{i}", []))
    elif isinstance(data, dict):
        for key, value in data.items():
            order.extend(get_twist_text_with_key(value, f"{key_prefix}-{key}", []))

    return order


def send_request(method="get", endpoint="", payload=None):
    headers = {"x-auth-token": STORY3_API_KEY}
    response = ""
    if method == "get":
        response = requests.get(endpoint, headers=headers)
        response = response.json()

    if method == "post":
        response = requests.post(endpoint, json=payload, headers=headers)
        response = response.json()

    if method == "patch":
        response = requests.patch(endpoint, json=payload, headers=headers)
        response = response.json()

    return response


def format_llm_output(response):
    for char_ in ["'", "```json", "```"]:
        response = response.replace(char_, "")

    response = json.loads(response)

    return response


def create_story(story_title, story_body):
    logging.info("Creating story")
    response = {}
    try:
        endpoint = STORY3_API_ENDPOINTS.get("create_story").get("endpoint")
        payload = STORY3_API_ENDPOINTS.get("create_story").get("payload")

        payload["title"] = story_title
        payload["body"] = story_body

        response = send_request("post", endpoint=endpoint, payload=payload)
    except Exception:
        logging.exception("Error in create story")

    return response


def create_twist(parent_hash, twist_body):
    response = {}
    try:
        if twist_body:
            logging.info("Creating twist")
            twist_title = twist_body[:50] + "...."
            endpoint = STORY3_API_ENDPOINTS.get("create_twist").get("endpoint")
            payload = STORY3_API_ENDPOINTS.get("create_twist").get("payload")

            payload["hashParentId"] = parent_hash
            payload["title"] = twist_title
            payload["body"] = twist_body
            payload["isExtraTwist"] = True

            response = send_request("post", endpoint=endpoint, payload=payload)
            _ = publish_twist(response.get("hashId"))
            logging.info(
                f"Created twist hash - {response['hashId']} - status - {response['status']}"
            )
        else:
            logging.info("No twist body")
    except Exception:
        logging.exception(f"Error in create twist - hash - {parent_hash}")
    return response


def publish_twist(hash_id):
    response = {}
    try:
        endpoint = STORY3_API_ENDPOINTS.get("publish_twist").get("endpoint")

        endpoint = endpoint.replace("hashId", hash_id)

        response = send_request("post", endpoint=endpoint)
    except Exception:
        logging.exception(f"Error in publish twist - hash id {hash_id}")

    return response


def patch_story(hash_id, genre, tags):
    response = {}
    try:
        endpoint = STORY3_API_ENDPOINTS.get("patch_story").get("endpoint")

        endpoint = endpoint.replace("hashId", hash_id)

        payload = STORY3_API_ENDPOINTS.get("patch_story").get("payload")

        payload["genre"] = genre
        payload["tags"] = tags
        response = send_request("patch", endpoint=endpoint, payload=payload)
    except Exception:
        logging.exception(
            f"Error in patch_story - hash id - {hash_id} - genre - {genre} - tags - {tags}"
        )

    return response


def patch_twist(hash_id):
    response = {}
    try:
        endpoint = STORY3_API_ENDPOINTS.get("patch_twist").get("endpoint")

        endpoint = endpoint.replace("hashId", hash_id)

        payload = STORY3_API_ENDPOINTS.get("patch_twist").get("payload")
        response = send_request("patch", endpoint=endpoint, payload=payload)
    except Exception:
        logging.exception(f"Error in patch twist - hash id - {hash_id}")

    return response


def get_story(hash_id):
    response = {}
    try:
        endpoint = STORY3_API_ENDPOINTS.get("get_story").get("endpoint")

        endpoint = endpoint.replace("hashId", hash_id)
        response = send_request("get", endpoint=endpoint)
    except Exception:
        logging.exception(f"Error in get story - hash id - {hash_id}")

    return response
