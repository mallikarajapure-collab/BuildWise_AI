import pytest
from services.llm_service import get_chatbot_response


@pytest.mark.parametrize("message", [
    "hello",
    "hi",
    "hey",
    "namaste",
])
def test_greetings(message):
    response = get_chatbot_response(message)
    assert isinstance(response, str)
    assert "BuildWise AI" in response


def test_project_suggestions():
    response = get_chatbot_response("Suggest a project")
    assert "project" in response.lower()


def test_skill_guidance():
    response = get_chatbot_response("What skills should I learn?")
    assert "Python" in response


def test_roadmap_guidance():
    response = get_chatbot_response("Give me a roadmap")
    assert "roadmap" in response.lower()
    assert "GitHub" in response


def test_internship_guidance():
    response = get_chatbot_response("How do I prepare for an internship?")
    assert "internship" in response.lower()


def test_thank_you():
    response = get_chatbot_response("Thank you")
    assert "welcome" in response.lower()


@pytest.mark.parametrize("message", ["", "   ", "\n\t"])
def test_empty_input(message):
    response = get_chatbot_response(message)
    assert "type a question" in response.lower()


def test_unknown_question_has_fallback():
    response = get_chatbot_response("What is the weather on Mars?")
    assert isinstance(response, str)
    assert len(response) > 0
    assert "project ideas" in response.lower()


def test_non_string_input():
    response = get_chatbot_response(None)
    assert "type a question" in response.lower()
