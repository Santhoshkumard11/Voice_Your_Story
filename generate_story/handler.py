import json
import azure.functions as func

from generate_story.llm_helper import generate_complete_story_body_from_llm
from generate_story.utils import format_llm_output


def handle_generate_story(story_text):
    # response = generate_complete_story_body_from_llm(story_text)
    # formatted_response = format_llm_output(response)

    return func.HttpResponse(
        json.dumps(
            {
                "message": "Successfully published the story",
                "story_link": "",
            }
        ),
        status_code=200,
    )
