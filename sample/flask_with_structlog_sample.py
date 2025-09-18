import traceback

from typing import Any

import shortuuid
import structlog

from app import structlog_utils
from flask import Flask, request, request_started


logger = structlog_utils.get_logger(name=__name__)


def bind_request_details(sender: Flask, **extras: dict[str, Any]) -> None:
    """Bind request details such as request_id to structlog contextvars at the start of a Flask request.

    Parameters
    ----------
    sender : Flask
        The Flask application instance sending the signal.
    **extras : dict[str, Any]
        Additional keyword arguments passed by the signal.

    Returns
    -------
    None

    """
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request.json.get("request_id", None),
    )


http_app = Flask(__name__)
request_started.connect(bind_request_details, http_app)


@http_app.route("/api/v1/test", methods=["POST"])
def test_request_id() -> dict[str, Any]:
    """Handle POST requests to /api/v1/test by logging a test message and returning the request_id.

    Returns
    -------
    dict[str, Any]
        A dictionary containing the request_id or an error message.

    """
    payload: dict[Any, Any] = request.json
    try:
        request_id = payload.get("request_id")
        logger.info(f"{shortuuid.uuid()} this is test message")
    except Exception as e:
        logger.info(e)
        logger.error(traceback.format_exc())
        return {"error": str(e)}
    return {"request_id": request_id}
