import io
import json

import pytest
import requests

import rubikai
from rubikai import error


# FILE TESTS
def test_file_upload():
    result = rubikai.File.create(
        file=io.StringIO(
            json.dumps({"prompt": "test file data", "completion": "tada"})
        ),
        purpose="fine-tune",
    )
    assert result.purpose == "fine-tune"
    assert "id" in result

    result = rubikai.File.retrieve(id=result.id)
    assert result.status == "uploaded"


# CHAT COMPLETION TESTS
def test_chat_completions():
    result = rubikai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello!"}]
    )
    assert len(result.choices) == 1


def test_chat_completions_multiple():
    result = rubikai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello!"}], n=5
    )
    assert len(result.choices) == 5


def test_chat_completions_streaming():
    result = None
    events = rubikai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}],
        stream=True,
    )
    for result in events:
        assert len(result.choices) == 1


# COMPLETION TESTS
def test_completions():
    result = rubikai.Completion.create(prompt="This was a test", n=5, engine="ada")
    assert len(result.choices) == 5


def test_completions_multiple_prompts():
    result = rubikai.Completion.create(
        prompt=["This was a test", "This was another test"], n=5, engine="ada"
    )
    assert len(result.choices) == 10


def test_completions_model():
    result = rubikai.Completion.create(prompt="This was a test", n=5, model="ada")
    assert len(result.choices) == 5
    assert result.model.startswith("ada")


def test_timeout_raises_error():
    # A query that should take awhile to return
    with pytest.raises(error.Timeout):
        rubikai.Completion.create(
            prompt="test" * 1000,
            n=10,
            model="ada",
            max_tokens=100,
            request_timeout=0.01,
        )


def test_timeout_does_not_error():
    # A query that should be fast
    rubikai.Completion.create(
        prompt="test",
        model="ada",
        request_timeout=10,
    )


def test_user_session():
     with requests.Session() as session:
        rubikai.requestssession = session

        completion = rubikai.Completion.create(
            prompt="hello world",
            model="ada",
        )
        assert completion


def test_user_session_factory():
    def factory():
        session = requests.Session()
        session.mount(
            "https://",
            requests.adapters.HTTPAdapter(max_retries=4),
        )
        return session

    rubikai.requestssession = factory

    completion = rubikai.Completion.create(
        prompt="hello world",
        model="ada",
    )
    assert completion
