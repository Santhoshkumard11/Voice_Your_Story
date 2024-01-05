STORY3_HOST_NAME = "https://story3.com"
STORY3_API_VERSION = "v2"
MAX_STORY_TOKEN = 4_000

STORY3_API_ENDPOINTS = {
    "create_story": f"{STORY3_HOST_NAME}/api/{STORY3_API_VERSION}/stories",
    "create_twist": f"{STORY3_HOST_NAME}/api/{STORY3_API_VERSION}/twists",
    "publish_twist": f"{STORY3_HOST_NAME}/api/{STORY3_API_VERSION}/twists/hashId/publish",
}

STORY_OUTPUT_TEMPLATE = """
{
    "story_title": "<story title>",
    "story_body": "<story body>",
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
        "1_2": [
            "<twist text>",
            {
                "1_2_1": [
                    "<twist text>",
                    {}
                ]
            }
        ],
        "1_3": [
            "<twist text>",
            {}
        ]
    }
}
"""


PROMPT_TEMPLATE = """
Use the below starting part of a story text and create a complete story with a minimum of 2 twists - 1_2, 1_3 and 2 level deep in each twist.
The stories should be natural and should resemble a human mindset while writing it.
There has to be a continuation between 1 and 1_2 or 1 and 1_3, after 1, the story has a twist, user can select 1_2 or 1_3 and go further deep.
Each twist should be at least 50 words and the main story should be around 200 words.
Just return the json output and nothing else, no triple quotes.

Output Format:
The output should be a json.

{json_output_template}

Story Text:
{story_text}
"""
