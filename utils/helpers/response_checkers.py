import requests
from pydantic import ValidationError
from utils.helpers.logger import gen_logger

logger = gen_logger(__name__)


def check_code(responce, expected_code):
    try:
        assert responce.status_code == expected_code
    except (TypeError, KeyError, NotImplementedError) as e:
        logger.error(f"Error {type(e).__name__}: {e}")


def validate_schema(response, schema, context=None):
    try:
        schema.model_validate(response, context=context)
    except ValidationError as e:
        assert False, f"Not correct {e}"
