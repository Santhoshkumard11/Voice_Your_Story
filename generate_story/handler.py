import logging
import json

from generate_story.llm_helper import generate_complete_story_body_from_llm
from generate_story.utils import (
    create_twist,
    create_story,
    patch_story,
    publish_twist,
    format_twists_text,
)


def handle_generate_story(story_text):
    formatted_response = generate_complete_story_body_from_llm(story_text)
    logging.info(f"Got response from LLM - {formatted_response}")

    logging.info("Got formatted output from llm")

    # use recursion to update the twists in the respective place
    # use try except to make sure each step is complete and send proper error message to UI
    # first make things work - hardcode to get the values and publish a story
    # make things dynamic after - we need to send the story on LinkedIn to make sure we get more followers

    story_title, story_body, genre, tags = (
        formatted_response.get("story_title"),
        formatted_response.get("story_body")[:1199],
        formatted_response.get("genre"),
        formatted_response.get("tags")[:6],
    )

    twist_dict = formatted_response.get("twists")
    formatted_twists = format_twists_text(twist_dict)

    response_create_story = create_story(story_title, story_body)
    story_hash_id = response_create_story.get("hashId")
    logging.info(
        f"Created story with hash id - {story_hash_id} - {response_create_story}"
    )
    _ = patch_story(story_hash_id, genre, tags)

    level_1_twist_1 = formatted_twists.get("1")
    level_1_twist_2 = formatted_twists.get("2")
    level_1_twist_3 = formatted_twists.get("3")

    level_2_twist_1 = formatted_twists.get("1_1")
    level_2_twist_2 = formatted_twists.get("2_1")

    level_3_twist_1 = formatted_twists.get("1_1_1")
    level_3_twist_2 = formatted_twists.get("1_1_2")

    level_4_twist_2 = formatted_twists.get("1_1_2_1")

    response_l1_t1 = create_twist(story_hash_id, level_1_twist_1)
    response_l1_t2 = create_twist(story_hash_id, level_1_twist_2)
    response_l1_t3 = create_twist(story_hash_id, level_1_twist_3)

    response_l2_t1 = create_twist(response_l1_t1.get("hashId"), level_2_twist_1)
    response_l2_t2 = create_twist(response_l1_t2.get("hashId"), level_2_twist_2)

    response_l3_t1 = create_twist(response_l2_t1.get("hashId"), level_3_twist_1)
    response_l3_t2 = create_twist(response_l2_t1.get("hashId"), level_3_twist_2)

    response_l4_t1 = create_twist(response_l3_t2.get("hashId"), level_4_twist_2)

    _ = publish_twist(story_hash_id)
    logging.info("Successfully published story")

    return json.dumps(
        {
            "message": "Successfully published the story",
            "story_link": "",
        }
    )
