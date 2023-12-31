import azure.functions as func
import logging
import mimetypes

from static_page_render.constants import ALLOWED_RENDER_FILE_NAME_LIST

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

    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get("name")

    if name:
        return func.HttpResponse(
            f"Hello, {name}. This HTTP triggered function executed successfully."
        )
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200,
        )
