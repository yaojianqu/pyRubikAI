import time

from rubikai import util, error
from rubikai.api_resources.abstract.engine_api_resource import EngineAPIResource
from rubikai.error import TryAgain


class Edit(EngineAPIResource):
    OBJECT_NAME = "edits"

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Creates a new edit for the provided input, instruction, and parameters.
        """
        start = time.time()
        timeout = kwargs.pop("timeout", None)

        api_type = kwargs.pop("api_type", None)
        typed_api_type = cls._get_api_type_and_version(api_type=api_type)[0]
        if typed_api_type in (util.ApiType.AZURE, util.ApiType.AZURE_AD):
            raise error.InvalidAPIType(
                "This operation is not supported by the Azure RubikAI API yet."
            )

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
        Creates a new edit for the provided input, instruction, and parameters.
        """
        start = time.time()
        timeout = kwargs.pop("timeout", None)

        api_type = kwargs.pop("api_type", None)
        typed_api_type = cls._get_api_type_and_version(api_type=api_type)[0]
        if typed_api_type in (util.ApiType.AZURE, util.ApiType.AZURE_AD):
            raise error.InvalidAPIType(
                "This operation is not supported by the Azure RubikAI API yet."
            )

        while True:
            try:
                return await super().acreate(*args, **kwargs)
            except TryAgain as e:
                if timeout is not None and time.time() > start + timeout:
                    raise

                util.log_info("Waiting for model to warm up", error=e)
