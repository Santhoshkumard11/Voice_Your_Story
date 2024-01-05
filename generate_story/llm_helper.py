from openai import AzureOpenAI
import os
import logging
from .constants import MAX_STORY_TOKEN

AZURE_OPENAI_API_VERSION = "2023-12-01-preview"
AZURE_OPENAI_DEPLOYMENT_NAME = "sandy_gpt_4_model"


def create_azure_openai_client():
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )


def generate_complete_story_body_from_llm(prompt_text):
    client = create_azure_openai_client()
    logging.info("Connected to Azure OpenAI Service")

    final_prompt = [
        {
            "role": "system",
            "content": "Assume you are the greatest story teller of all time",
        },
        {"role": "user", "content": prompt_text},
    ]

    logging.info("Sending a test completion job")

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        prompt=final_prompt,
        max_tokens=MAX_STORY_TOKEN,
    )
    response_text = response.choices[0].message.content
    total_tokens_used = response.usage.total_tokens

    logging.info(f"Total Tokens used: {total_tokens_used}")

    return response_text
