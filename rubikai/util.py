import logging
import os
import re
import sys
from enum import Enum
from typing import Optional

import rubikai

RUBIKAI_LOG = os.environ.get("RUBIKAI_LOG")

logger = logging.getLogger("rubikai")

__all__ = [
    "log_info",
    "log_debug",
    "log_warn",
    "logfmt",
]

api_key_to_header = (
    lambda api, key: {"Authorization": f"{key}"}
    if api in (ApiType.RUBIK_AI, ApiType.AZURE_AD)
    else {"api-key": f"{key}"}
)


class ApiType(Enum):
    AZURE = 1
    RUBIK_AI = 2
    AZURE_AD = 3

    @staticmethod
    def from_str(label):
        if label.lower() == "azure":
            return ApiType.AZURE
        elif label.lower() in ("azure_ad", "azuread"):
            return ApiType.AZURE_AD
        elif label.lower() in ("rubik_ai", "rubikai"):
            return ApiType.RUBIK_AI
        else:
            raise rubikai.error.InvalidAPIType(
                "The API type provided in invalid. Please select one of the supported API types: 'azure', 'azure_ad', 'rubik_ai'"
            )


def _console_log_level():
    if rubikai.log in ["debug", "info"]:
        return rubikai.log
    elif RUBIKAI_LOG in ["debug", "info"]:
        return RUBIKAI_LOG
    else:
        return None


def log_debug(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() == "debug":
        print(msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() in ["debug", "info"]:
        print(msg, file=sys.stderr)
    logger.info(msg)


def log_warn(message, **params):
    msg = logfmt(dict(message=message, **params))
    print(msg, file=sys.stderr)
    logger.warn(msg)


def logfmt(props):
    def fmt(key, val):
        # Handle case where val is a bytes or bytesarray
        if hasattr(val, "decode"):
            val = val.decode("utf-8")
        # Check if val is already a string to avoid re-encoding into ascii.
        if not isinstance(val, str):
            val = str(val)
        if re.search(r"\s", val):
            val = repr(val)
        # key should already be a string
        if re.search(r"\s", key):
            key = repr(key)
        return "{key}={val}".format(key=key, val=val)

    return " ".join([fmt(key, val) for key, val in sorted(props.items())])


def get_object_classes():
    # This is here to avoid a circular dependency
    from rubikai.object_classes import OBJECT_CLASSES

    return OBJECT_CLASSES


def convert_to_rubikai_object(
    resp,
    api_key=None,
    api_version=None,
    organization=None,
    engine=None,
    plain_old_data=False,
):
    # If we get a RubikAIResponse, we'll want to return a RubikAIObject.
    response_ms: Optional[int] = None
    if isinstance(resp, rubikai.rubikai_response.RubikAIResponse):
        organization = resp.organization
        response_ms = resp.response_ms
        resp = resp.data

    if plain_old_data:
        return resp
    elif isinstance(resp, list):
        return [
            convert_to_rubikai_object(
                i, api_key, api_version, organization, engine=engine
            )
            for i in resp
        ]
    elif isinstance(resp, dict) and not isinstance(resp, rubikai.rebik_object.RubikAIObject):
        resp = resp.copy()
        klass_name = resp.get("object")
        if isinstance(klass_name, str):
            klass = get_object_classes().get(klass_name, rubikai.rebik_object.RubikAIObject)
        else:
            klass = rubikai.rebik_object.RubikAIObject

        return klass.construct_from(
            resp,
            api_key=api_key,
            api_version=api_version,
            organization=organization,
            response_ms=response_ms,
            engine=engine,
        )
    else:
        return resp


def convert_to_dict(obj):
    """Converts a RubikAIObject back to a regular dict.

    Nested RubikAIObjects are also converted back to regular dicts.

    :param obj: The RubikAIObject to convert.

    :returns: The RubikAIObject as a dict.
    """
    if isinstance(obj, list):
        return [convert_to_dict(i) for i in obj]
    # This works by virtue of the fact that RubikAIObjects _are_ dicts. The dict
    # comprehension returns a regular dict and recursively applies the
    # conversion to each value.
    elif isinstance(obj, dict):
        return {k: convert_to_dict(v) for k, v in obj.items()}
    else:
        return obj


def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def default_api_key() -> str:
    if rubikai.api_key_path:
        with open(rubikai.api_key_path, "rt") as k:
            api_key = k.read().strip()
            if not api_key.startswith("sk-"):
                raise ValueError(f"Malformed API key in {rubikai.api_key_path}.")
            return api_key
    elif rubikai.api_key is not None:
        return rubikai.api_key
    else:
        raise rubikai.error.AuthenticationError(
            "No API key provided. You can set your API key in code using 'rubikai.api_key = <API-KEY>', or you can set the environment variable RUBIKAI_API_KEY=<API-KEY>). If your API key is stored in a file, you can point the rubikai module at it with 'rubikai.api_key_path = <PATH>'. You can generate API keys in the RubikAI web interface. See https://platform.rubikai.com/account/api-keys for details."
        )
