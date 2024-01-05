import azure.functions as func
import logging
import mimetypes
import json

from static_page_render.constants import ALLOWED_RENDER_FILE_NAME_LIST
from generate_story.handler import handle_generate_story

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.function_name(name="speak_out")
@app.route(route="speak_out")
def speak_out(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Static page serving..")

    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get("name")

    path = "static_page_render/web"

    file_path = f"{path}/{name}"
    if name in ALLOWED_RENDER_FILE_NAME_LIST:
        # open the file and load the html file
        with open(file_path, "rb") as f:
            mimetype = mimetypes.guess_type(file_path)
            logging.info(f"Serving file - {name}")
            return func.HttpResponse(f.read(), mimetype=mimetype[0], status_code=200)
    else:
        return func.HttpResponse(
            f"{name} is not a valid file name to render!", status_code=400
        )


@app.function_name(name="generate_story")
@app.route(route="generate_story", auth_level=func.AuthLevel.FUNCTION)
def generate_story(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Generate Story endpoint hit!")

    story_text = ""

    try:
        req_body = req.get_json()
        story_text = req_body.get("storyText")

        logging.info(f"Received story text - {story_text[:100]}")

        response = handle_generate_story(story_text)

    except ValueError:
        response = func.HttpResponse(
            json.dumps(
                {
                    "message": "Error while trying to get the request body! Check if you've passed storyText in body"
                }
            ),
            status_code=400,
        )

    return response


@app.function_name(name="home")
@app.route(route="test", auth_level=func.AuthLevel.FUNCTION)
def home(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("The endpoint is working!!")
