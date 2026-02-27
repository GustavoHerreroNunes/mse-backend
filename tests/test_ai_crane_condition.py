import json
from unittest.mock import patch

import pytest

from reportlab_pages.utils.ai_crane_condition import ai_crane_condition

PATCH = "reportlab_pages.utils.ai_crane_condition.prompt_model"
FALLBACK = ["No further comments to be made."]

SAMPLE_DATA = {
    "external_cranes": "Fair",
    "wire": "Good",
    "sheaves": "Fair",
    "operation_condition": "Very Good",
}


class TestAiCraneCondition:

    def test_returns_exactly_three_observations(self):
        observations = ["Crane structure in fair condition.", "Wire ropes show adequate condition.", "Sheaves show minor wear."]
        with patch(PATCH, return_value=json.dumps(observations)) as mock_pm:
            result = ai_crane_condition(SAMPLE_DATA)
        assert result == observations
        assert len(result) == 3
        mock_pm.assert_called_once()

    def test_strips_markdown_json_code_fence(self):
        observations = ["Obs 1.", "Obs 2.", "Obs 3."]
        raw = f"```json\n{json.dumps(observations)}\n```"
        with patch(PATCH, return_value=raw):
            result = ai_crane_condition(SAMPLE_DATA)
        assert result == observations

    def test_passes_correct_max_tokens_to_prompt_model(self):
        observations = ["A.", "B.", "C."]
        with patch(PATCH, return_value=json.dumps(observations)) as mock_pm:
            ai_crane_condition(SAMPLE_DATA)
        assert mock_pm.call_args.kwargs["max_tokens"] == 250

    def test_passes_serialized_data_as_user_message(self):
        observations = ["A.", "B.", "C."]
        with patch(PATCH, return_value=json.dumps(observations)) as mock_pm:
            ai_crane_condition(SAMPLE_DATA)
        assert json.loads(mock_pm.call_args.kwargs["user"]) == SAMPLE_DATA

    def test_api_exception_returns_fallback(self):
        with patch(PATCH, side_effect=RuntimeError("Vertex AI unavailable")):
            result = ai_crane_condition(SAMPLE_DATA)
        assert result == FALLBACK

    def test_invalid_json_response_returns_fallback(self):
        with patch(PATCH, return_value="not json at all"):
            result = ai_crane_condition(SAMPLE_DATA)
        assert result == FALLBACK

    def test_response_not_a_list_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps("single string")):
            result = ai_crane_condition(SAMPLE_DATA)
        assert result == FALLBACK

    def test_two_items_instead_of_three_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps(["Obs 1.", "Obs 2."])):
            result = ai_crane_condition(SAMPLE_DATA)
        assert result == FALLBACK

    def test_four_items_instead_of_three_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps(["A.", "B.", "C.", "D."])):
            result = ai_crane_condition(SAMPLE_DATA)
        assert result == FALLBACK

    def test_list_with_non_strings_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps([1, 2, 3])):
            result = ai_crane_condition(SAMPLE_DATA)
        assert result == FALLBACK
