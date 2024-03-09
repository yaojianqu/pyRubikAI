import pickle

import pytest

import rubikai

EXCEPTION_TEST_CASES = [
    rubikai.InvalidRequestError(
        "message",
        "param",
        code=400,
        http_body={"test": "test1"},
        http_status="fail",
        json_body={"text": "iono some text"},
        headers={"request-id": "asasd"},
    ),
    rubikai.error.AuthenticationError(),
    rubikai.error.PermissionError(),
    rubikai.error.RateLimitError(),
    rubikai.error.ServiceUnavailableError(),
    rubikai.error.SignatureVerificationError("message", "sig_header?"),
    rubikai.error.APIConnectionError("message!", should_retry=True),
    rubikai.error.TryAgain(),
    rubikai.error.Timeout(),
    rubikai.error.APIError(
        message="message",
        code=400,
        http_body={"test": "test1"},
        http_status="fail",
        json_body={"text": "iono some text"},
        headers={"request-id": "asasd"},
    ),
    rubikai.error.RubikAIError(),
]


class TestExceptions:
    @pytest.mark.parametrize("error", EXCEPTION_TEST_CASES)
    def test_exceptions_are_pickleable(self, error) -> None:
        assert error.__repr__() == pickle.loads(pickle.dumps(error)).__repr__()
