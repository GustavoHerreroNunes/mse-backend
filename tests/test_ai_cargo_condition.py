import json
from unittest.mock import patch

import pytest

from reportlab_pages.utils.ai_cargo_condition import ai_cargo_condition

PATCH = "reportlab_pages.utils.ai_cargo_condition.prompt_model"
FALLBACK = ["No further comments to be made."]

SAMPLE_DATA = {
    "ranking_scratches": "Moderate",
    "ranking_dents": "Poor",
    "moisture": "Yes",
}


class TestAiCargoCondition:

    def test_returns_valid_observations(self):
        observations = ["Scratches noted on wood surfaces.", "Dents detected on crate panels."]
        with patch(PATCH, return_value=json.dumps(observations)) as mock_pm:
            result = ai_cargo_condition(SAMPLE_DATA)
        assert result == observations
        mock_pm.assert_called_once()

    def test_returns_up_to_six_observations(self):
        observations = [f"Observation {i}." for i in range(1, 7)]
        with patch(PATCH, return_value=json.dumps(observations)):
            result = ai_cargo_condition(SAMPLE_DATA)
        assert result == observations
        assert len(result) == 6

    def test_strips_markdown_json_code_fence(self):
        observations = ["Damage noted on exterior."]
        raw = f"```json\n{json.dumps(observations)}\n```"
        with patch(PATCH, return_value=raw):
            result = ai_cargo_condition(SAMPLE_DATA)
        assert result == observations

    def test_strips_plain_code_fence(self):
        observations = ["Structural integrity compromised."]
        raw = f"```\n{json.dumps(observations)}\n```"
        with patch(PATCH, return_value=raw):
            result = ai_cargo_condition(SAMPLE_DATA)
        assert result == observations

    def test_passes_correct_max_tokens_to_prompt_model(self):
        with patch(PATCH, return_value=json.dumps(["Obs."])) as mock_pm:
            ai_cargo_condition(SAMPLE_DATA)
        assert mock_pm.call_args.kwargs["max_tokens"] == 900

    def test_passes_serialized_data_as_user_message(self):
        with patch(PATCH, return_value=json.dumps(["Obs."])) as mock_pm:
            ai_cargo_condition(SAMPLE_DATA)
        assert json.loads(mock_pm.call_args.kwargs["user"]) == SAMPLE_DATA

    def test_api_exception_returns_fallback(self):
        with patch(PATCH, side_effect=RuntimeError("Vertex AI unavailable")):
            result = ai_cargo_condition(SAMPLE_DATA)
        assert result == FALLBACK

    def test_invalid_json_response_returns_fallback(self):
        with patch(PATCH, return_value="this is not json"):
            result = ai_cargo_condition(SAMPLE_DATA)
        assert result == FALLBACK

    def test_response_not_a_list_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps({"obs": "Damage noted."})):
            result = ai_cargo_condition(SAMPLE_DATA)
        assert result == FALLBACK

    def test_empty_list_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps([])):
            result = ai_cargo_condition(SAMPLE_DATA)
        assert result == FALLBACK

    def test_list_with_non_strings_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps([1, 2, 3])):
            result = ai_cargo_condition(SAMPLE_DATA)
        assert result == FALLBACK

    def test_list_exceeding_six_items_returns_fallback(self):
        observations = [f"Obs {i}." for i in range(7)]
        with patch(PATCH, return_value=json.dumps(observations)):
            result = ai_cargo_condition(SAMPLE_DATA)
        assert result == FALLBACK
