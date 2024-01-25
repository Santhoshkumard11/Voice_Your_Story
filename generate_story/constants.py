STORY3_HOST_NAME = "https://story3.com"
STORY3_API_VERSION = "v2"
MAX_STORY_TOKEN = 4_000

STORY3_API_ENDPOINTS = {
    "create_story": {
        "endpoint": f"{STORY3_HOST_NAME}/api/{STORY3_API_VERSION}/stories",
        "payload": {"title": "string", "body": "string"},
    },
    "create_twist": {
        "endpoint": f"{STORY3_HOST_NAME}/api/{STORY3_API_VERSION}/twists",
        "payload": {
            "hashParentId": "string",
            "isExtraTwist": True,
            "title": "string",
            "body": "string",
        },
    },
    "publish_twist": {
        "endpoint": f"{STORY3_HOST_NAME}/api/{STORY3_API_VERSION}/twists/hashId/publish"
    },
    "patch_story": {
        "endpoint": f"{STORY3_HOST_NAME}/api/{STORY3_API_VERSION}/stories/hashId",
        "payload": {"genre": "string", "tags": ["string"]},
    },
    "patch_twist": {
        "endpoint": f"{STORY3_HOST_NAME}/api/{STORY3_API_VERSION}/twists/hashId",
        "payload": {
            "monetization_option": "free",
        },
    },
    "get_story": {
        "endpoint": f"{STORY3_HOST_NAME}/api/{STORY3_API_VERSION}/stories/hashId",
    },
}

STORY_OUTPUT_TEMPLATE = """
{
    "story_title": "<story title>",
    "story_body": "<story body>",
    "genre": "<type of genre>",
    "tags": <list of tags>,
    "twists": {
        "1": [
            "<twist text>",
            {
                "1_1": [
                    "<twist text>",
                    {
                        "1_1_1": [
                            "<twist text>",
                            {}
                        ],
                        "1_1_2": [
                            "<twist text>",
                            {
                                "1_1_2_1": [
                                    "<twist text>",
                                    {}
                                ]
                            }
                        ]
                    }
                ]
            }
        ],
        "2": [
            "<twist text>",
            {
                "2_1": [
                    "<twist text>",
                    {}
                ]
            }
        ],
        "3": [
            "<twist text>",
            {}
        ]
    }
}
"""


PROMPT_TEMPLATE = """
Use the below starting part of a story text and create a complete story with a minimum of 2 twists - 1_2, 1_3 and 2 level deep in each twist.
The stories should be natural and should resemble a human mindset while writing it.
There has to be a continuation between 1_1 and 1_1_1, after 1, the story has a twist, user can select 1_2 or 1_3 and go further deep.
Each twist should be at least 100 words and the main story should be around 300 words.
Add more text to the story and twists to make sure the words requirement is met.
Just return the json output and nothing else, no triple quotes.

Add relevant tags to the story from the below list,
Drama, Fantasy, Fiction, Psychological, Romance, Adventure, Myths, Friendship, Suspense, Dystopian, Young Adult, Mystery, Narrative, Science,

Output Format:
The output should be a json.

{json_output_template}

Story Text:
{story_text}
"""
