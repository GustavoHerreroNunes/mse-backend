import json
from unittest.mock import patch

import pytest

from reportlab_pages.utils.ai_stowage_condition import ai_stowage_condition

PATCH = "reportlab_pages.utils.ai_stowage_condition.prompt_model"
FALLBACK = ["No further comments to be made."]
NO_FINDINGS = ["No negative findings observed."]
TIPO = "stowage inspection"


# --- Data helpers ---

def all_pass():
    """All stowage fields considered passing."""
    return {
        "proper_stowage": "Yes",
        "obstructions_stowage": "Yes",
        "proper_plating": "Yes",
        "surrounded_risks": "Yes",
        # "Hot works" / "There are" fields — "No" = no issue
        "damages_internal": "No",
        "contaminant": "No",
    }

def with_findings():
    """Stowage fields with negative findings."""
    return {
        "proper_stowage": "No",      # positive field → flagged when != Yes
        "contaminant": "Yes",        # "There are" field → flagged when == Yes
    }


class TestAiStowageCondition:

    def test_no_negative_findings_returns_early(self):
        with patch(PATCH) as mock_pm:
            result = ai_stowage_condition(all_pass(), TIPO)
        assert result == NO_FINDINGS
        mock_pm.assert_not_called()

    def test_does_not_apply_treated_as_passing(self):
        data = {**all_pass(), "proper_stowage": "Does Not Apply"}
        with patch(PATCH) as mock_pm:
            result = ai_stowage_condition(data, TIPO)
        assert result == NO_FINDINGS
        mock_pm.assert_not_called()

    def test_valid_response_returned(self):
        observations = ["Cargo improperly stowed.", "Contaminants detected near cargo area."]
        with patch(PATCH, return_value=json.dumps(observations)):
            result = ai_stowage_condition(with_findings(), TIPO)
        assert result == observations

    def test_api_exception_returns_fallback(self):
        with patch(PATCH, side_effect=RuntimeError("API error")):
            result = ai_stowage_condition(with_findings(), TIPO)
        assert result == FALLBACK

    def test_invalid_json_returns_fallback(self):
        with patch(PATCH, return_value="not json"):
            result = ai_stowage_condition(with_findings(), TIPO)
        assert result == FALLBACK

    def test_wrong_format_not_list_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps({"obs": "value"})):
            result = ai_stowage_condition(with_findings(), TIPO)
        assert result == FALLBACK

    def test_empty_list_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps([])):
            result = ai_stowage_condition(with_findings(), TIPO)
        assert result == FALLBACK

    def test_list_exceeding_six_items_returns_fallback(self):
        observations = [f"Obs {i}." for i in range(7)]
        with patch(PATCH, return_value=json.dumps(observations)):
            result = ai_stowage_condition(with_findings(), TIPO)
        assert result == FALLBACK

    def test_list_with_non_strings_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps([1, 2, 3])):
            result = ai_stowage_condition(with_findings(), TIPO)
        assert result == FALLBACK

    def test_passes_correct_max_tokens(self):
        with patch(PATCH, return_value=json.dumps(["Obs."])) as mock_pm:
            ai_stowage_condition(with_findings(), TIPO)
        assert mock_pm.call_args.kwargs["max_tokens"] == 800

    def test_tipo_included_in_system_prompt(self):
        """The tipo argument should appear in the system instruction."""
        custom_tipo = "bulk cargo survey"
        with patch(PATCH, return_value=json.dumps(["Obs."])) as mock_pm:
            ai_stowage_condition(with_findings(), custom_tipo)
        assert custom_tipo in mock_pm.call_args.kwargs["system"]

    def test_strips_markdown_code_fence(self):
        observations = ["Dunnage improperly placed."]
        raw = f"```json\n{json.dumps(observations)}\n```"
        with patch(PATCH, return_value=raw):
            result = ai_stowage_condition(with_findings(), TIPO)
        assert result == observations

    def test_passes_only_failing_fields_as_user_message(self):
        """Only flagged fields should be forwarded to the model."""
        data = {
            "proper_stowage": "No",        # flagged
            "contaminant": "Yes",          # flagged
            "obstructions_stowage": "Yes", # passing — should NOT appear
            "damages_internal": "No",      # passing — should NOT appear
        }
        with patch(PATCH, return_value=json.dumps(["Obs."])) as mock_pm:
            ai_stowage_condition(data, TIPO)
        sent = json.loads(mock_pm.call_args.kwargs["user"])
        assert "obstructions_stowage" not in sent
        assert "damages_internal" not in sent
        assert len(sent) == 2
