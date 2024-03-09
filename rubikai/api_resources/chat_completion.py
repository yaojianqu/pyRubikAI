import time

from rubikai import util
from rubikai.api_resources.abstract.engine_api_resource import EngineAPIResource
from rubikai.error import TryAgain


class ChatCompletion(EngineAPIResource):
    engine_required = False
    OBJECT_NAME = "chat.completions"

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Creates a new chat completion for the provided messages and parameters.

        See https://platform.rubikai.com/docs/api-reference/chat/create
        for a list of valid parameters.
        """
        start = time.time()
        timeout = kwargs.pop("timeout", None)
        if "object_name" in kwargs:
            cls.OBJECT_NAME = kwargs.pop("object_name")
        if "model" not in kwargs:
            new_kwargs = {"model": "rubik6-chat"}  # 新的参数
            kwargs.update(new_kwargs)
        while True:
            try:
                return super().create(*args, **kwargs)
            except TryAgain as e:
                if timeout is not None and time.time() > start + timeout:
                    raise

                util.log_info("Waiting for model to warm up", error=e)

    @classmethod
    async def acreate(cls, *args, **kwargs):
        """
        Creates a new chat completion for the provided messages and parameters.

        See https://platform.rubikai.com/docs/api-reference/chat/create
        for a list of valid parameters.
        """
        start = time.time()
        timeout = kwargs.pop("timeout", None)
        if "object_name" in kwargs:
            cls.OBJECT_NAME = kwargs.pop("object_name")
        if "model" not in kwargs:
            new_kwargs = {"model": "rubik6-chat"}  # 新的参数
            kwargs.update(new_kwargs)
        while True:
            try:
                return await super().acreate(*args, **kwargs)
            except TryAgain as e:
                if timeout is not None and time.time() > start + timeout:
                    raise

                util.log_info("Waiting for model to warm up", error=e)

    @classmethod
    def dealRequest(cls, *args, **kwargs):
        """
        Creates a new chat completion for the provided messages and parameters.

        See https://platform.rubikai.com/docs/api-reference/chat/create
        for a list of valid parameters.
        """
        start = time.time()
        timeout = kwargs.pop("timeout", None)

        if "object_name" in kwargs:
            cls.OBJECT_NAME = kwargs.pop("object_name")
        if "model" not in kwargs:
            new_kwargs = {"model": "rubik6-chat"}  # 新的参数
            kwargs.update(new_kwargs)
        while True:
            try:
                return super().create(*args, **kwargs)
            except TryAgain as e:
                if timeout is not None and time.time() > start + timeout:
                    raise

                util.log_info("Waiting for model to warm up", error=e)