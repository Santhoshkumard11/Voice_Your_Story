from time import time
from openai import AzureOpenAI
import os
import logging
from .constants import (
    MAX_STORY_TOKEN,
    STORY_OUTPUT_TEMPLATE,
    PROMPT_TEMPLATE,
    AZURE_OPENAI_COST,
)

from .utils import format_llm_output

AZURE_OPENAI_API_VERSION = "2023-12-01-preview"
AZURE_OPENAI_DEPLOYMENT_NAME = "sandy_gpt_4_model"


def create_azure_openai_client():
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )


def generate_complete_story_body_from_llm(story_text):
    start_time = time()
    client = create_azure_openai_client()
    logging.info("Connected to Azure OpenAI Service")

    prompt_text = PROMPT_TEMPLATE.format(
        story_text=story_text, json_output_template=STORY_OUTPUT_TEMPLATE
    )

    final_prompt = [
        {
            "role": "system",
            "content": "Assume you are the greatest story teller of all time",
        },
        {"role": "user", "content": prompt_text},
    ]

    logging.info("Sending a completion job")

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=final_prompt,
        max_tokens=MAX_STORY_TOKEN,
    )
    response_text = response.choices[0].message.content
    (
        total_tokens_used,
        prompt_tokens,
        completion_tokens,
    ) = (
        response.usage.total_tokens,
        response.usage.prompt_tokens,
        response.usage.completion_tokens,
    )
    end_time = time()
    formatted_response_time = round(end_time - start_time, 2)
    logging.info(
        f"""Response time - {formatted_response_time}s - Total Tokens used: {total_tokens_used}
        Response:{response_text[:100]}"""
    )
    response_text = format_llm_output(response_text)

    response_text["total_tokens"] = total_tokens_used
    response_text["response_time"] = formatted_response_time
    response_text["cost"] = (prompt_tokens * 0.001) * AZURE_OPENAI_COST.get(
        "prompt"
    ) + (completion_tokens * 0.001) * AZURE_OPENAI_COST.get("completion")

    return response_text
