import json
from unittest.mock import patch

import pytest

from reportlab_pages.utils.ai_rigging_condition import ai_rigging_condition

PATCH = "reportlab_pages.utils.ai_rigging_condition.prompt_model"
FALLBACK = ["No further comments to be made."]
NO_FINDINGS = ["No negative findings observed."]


# --- Data helpers ---

def all_pass():
    """All rigging operation fields considered passing."""
    return {
        "elements_accordance": "Yes",
        "elements_fitted": "Yes",
        "safety_devices": "Yes",
        "beginning_inclination": "Yes",
        "has_pictures_elements": "Yes",
        "has_pictures_beginning": "Yes",
        "has_pictures_overall": "Yes",
        "has_pictures_stowage": "Yes",
        # "Are there" fields — "No" means no issue
        "twisted_line": "No",
        "slings_contact": "No",
        "during_inclination": "No",
    }

def with_findings():
    """Rigging fields with negative findings."""
    return {
        "elements_accordance": "No",    # positive field → flagged when != Yes
        "twisted_line": "Yes",          # "Are there" field → flagged when == Yes
        "slings_contact": "Yes",
    }


class TestAiRiggingCondition:

    def test_no_negative_findings_returns_early(self):
        with patch(PATCH) as mock_pm:
            result = ai_rigging_condition(all_pass())
        assert result == NO_FINDINGS
        mock_pm.assert_not_called()

    def test_does_not_apply_treated_as_passing(self):
        data = {**all_pass(), "elements_accordance": "Does Not Apply"}
        with patch(PATCH) as mock_pm:
            result = ai_rigging_condition(data)
        assert result == NO_FINDINGS
        mock_pm.assert_not_called()

    def test_valid_response_returned(self):
        observations = ["Lifting lines were found twisted during operation.", "Sling contact with sharp edge detected."]
        with patch(PATCH, return_value=json.dumps(observations)):
            result = ai_rigging_condition(with_findings())
        assert result == observations

    def test_api_exception_returns_fallback(self):
        with patch(PATCH, side_effect=RuntimeError("API error")):
            result = ai_rigging_condition(with_findings())
        assert result == FALLBACK

    def test_invalid_json_returns_fallback(self):
        with patch(PATCH, return_value="not json"):
            result = ai_rigging_condition(with_findings())
        assert result == FALLBACK

    def test_wrong_format_not_list_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps({"obs": "value"})):
            result = ai_rigging_condition(with_findings())
        assert result == FALLBACK

    def test_empty_list_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps([])):
            result = ai_rigging_condition(with_findings())
        assert result == FALLBACK

    def test_list_exceeding_six_items_returns_fallback(self):
        observations = [f"Obs {i}." for i in range(7)]
        with patch(PATCH, return_value=json.dumps(observations)):
            result = ai_rigging_condition(with_findings())
        assert result == FALLBACK

    def test_list_with_non_strings_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps([1, 2, 3])):
            result = ai_rigging_condition(with_findings())
        assert result == FALLBACK

    def test_passes_correct_max_tokens(self):
        with patch(PATCH, return_value=json.dumps(["Obs."])) as mock_pm:
            ai_rigging_condition(with_findings())
        assert mock_pm.call_args.kwargs["max_tokens"] == 1200

    def test_strips_markdown_code_fence(self):
        observations = ["Rigging elements not in accordance with lifting plan."]
        raw = f"```json\n{json.dumps(observations)}\n```"
        with patch(PATCH, return_value=raw):
            result = ai_rigging_condition(with_findings())
        assert result == observations

    def test_passes_filtered_fields_as_user_message(self):
        """Only flagged fields should reach prompt_model, not the full data dict."""
        data = {
            "elements_accordance": "No",   # flagged
            "twisted_line": "Yes",         # flagged
            "elements_fitted": "Yes",      # passing — should NOT appear
            "slings_contact": "No",        # passing — should NOT appear
        }
        with patch(PATCH, return_value=json.dumps(["Obs."])) as mock_pm:
            ai_rigging_condition(data)
        sent = json.loads(mock_pm.call_args.kwargs["user"])
        # Passing fields must not be forwarded to the model
        assert "elements_fitted" not in sent
        assert "slings_contact" not in sent
        # Failing fields must be forwarded
        assert len(sent) == 2
