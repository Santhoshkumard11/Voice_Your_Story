import logging
import json

from generate_story.llm_helper import generate_complete_story_body_from_llm
from generate_story.utils import (
    create_twist,
    create_story,
    get_story,
    patch_story,
    patch_twist,
    publish_twist,
    format_twists_text,
)


def handle_generate_story(story_text):
    formatted_response = generate_complete_story_body_from_llm(story_text)
    logging.info(f"Got response from LLM - {formatted_response}")

    logging.info("Got formatted output from llm")

    response_time, total_tokens, cost = (
        formatted_response.get("response_time"),
        formatted_response.get("total_tokens"),
        formatted_response.get("cost"),
    )

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
    _ = patch_twist(response_l1_t1.get("hashId"))
    response_l1_t2 = create_twist(story_hash_id, level_1_twist_2)
    _ = patch_twist(response_l1_t2.get("hashId"))
    response_l1_t3 = create_twist(story_hash_id, level_1_twist_3)
    _ = patch_twist(response_l1_t3.get("hashId"))

    response_l2_t1 = create_twist(response_l1_t1.get("hashId"), level_2_twist_1)
    response_l2_t2 = create_twist(response_l1_t2.get("hashId"), level_2_twist_2)

    response_l3_t1 = create_twist(response_l2_t1.get("hashId"), level_3_twist_1)
    response_l3_t2 = create_twist(response_l2_t1.get("hashId"), level_3_twist_2)

    response_l4_t1 = create_twist(response_l3_t2.get("hashId"), level_4_twist_2)

    _ = publish_twist(story_hash_id)
    logging.info("Successfully published story")

    story_details = get_story(story_hash_id)
    story_summary = story_details.get("path")[0].get("summary")

    story_url = f"https://story3.com/story_about+{story_summary}"

    return json.dumps(
        {
            "message": "Successfully published the story",
            "story_title": story_title,
            "story_link": story_url,
            "response_time": response_time,
            "total_tokens": total_tokens,
            "cost": cost,
        }
    )
