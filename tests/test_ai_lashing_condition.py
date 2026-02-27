import json
from unittest.mock import patch, MagicMock

import pytest

from reportlab_pages.utils.ai_lashing_condition import ai_lashing_condition

PATCH = "reportlab_pages.utils.ai_lashing_condition.prompt_model"
FALLBACK = ["Overall, the lashing material was determined to be in satisfactory operational condition."]
NO_FINDINGS = ["No negative findings observed."]

# --- Data helpers ---

def wire_ropes_all_pass():
    """All Wire Ropes fields considered passing — no findings expected."""
    return {
        "lashing_plan": "Yes",
        "lashing_items": "Yes",
        "lashing_material": "Yes",
        "lashing_condition": "Yes",
        "conclusion_wires_suitable": "Yes",
        "lashing_wires_acceptance": "Yes",
        # defect fields left as "No" — non-positive, "Yes" would flag them
        "broken_wires": "No",
        "corrosion_wires_visible": "No",
        "deformation_wires_caging": "No",
    }

def wire_ropes_with_findings():
    """Wire Ropes fields with negative findings."""
    return {
        "lashing_plan": "No",          # positive field → flagged when != Yes
        "broken_wires": "Yes",         # non-positive → flagged when == Yes
        "corrosion_wires_visible": "Yes",
    }

def shackles_all_pass():
    """All Shackles fields considered passing."""
    return {
        "lashing_plan": "Yes",
        "lashing_items": "Yes",
        "lashing_material": "Yes",
        "lashing_condition": "Yes",
        "visible_mark": "Yes",
        "visible_grade_number": "Yes",
        "visible_limit": "Yes",
        "compatible_pin": "Yes",
        "shackle_pin": "Yes",
        "tightened_pin": "Yes",
        "present_pin": "Yes",
        "lashing_shackles_acceptance": "Yes",
        "fractures": "No",
        "deformations": "No",
        "corrosion": "No",
        "wear": "No",
        "notches": "No",
    }

def shackles_with_findings():
    return {
        "lashing_plan": "No",
        "fractures": "Yes",
    }


class TestAiLashingConditionWireRopes:

    def test_no_negative_findings_returns_early(self):
        with patch(PATCH) as mock_pm:
            result = ai_lashing_condition(wire_ropes_all_pass(), "Wire Ropes")
        assert result == NO_FINDINGS
        mock_pm.assert_not_called()

    def test_does_not_apply_treated_as_passing(self):
        data = {**wire_ropes_all_pass(), "lashing_plan": "Does Not Apply"}
        with patch(PATCH) as mock_pm:
            result = ai_lashing_condition(data, "Wire Ropes")
        assert result == NO_FINDINGS
        mock_pm.assert_not_called()

    def test_valid_response_returned(self):
        observations = ["Wire rope shows visible corrosion.", "Lashing plan not applied."]
        with patch(PATCH, return_value=json.dumps(observations)):
            result = ai_lashing_condition(wire_ropes_with_findings(), "Wire Ropes")
        assert result == observations

    def test_api_exception_returns_fallback(self):
        with patch(PATCH, side_effect=RuntimeError("API error")):
            result = ai_lashing_condition(wire_ropes_with_findings(), "Wire Ropes")
        assert result == FALLBACK

    def test_invalid_json_returns_fallback(self):
        with patch(PATCH, return_value="not json"):
            result = ai_lashing_condition(wire_ropes_with_findings(), "Wire Ropes")
        assert result == FALLBACK

    def test_wrong_format_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps({"obs": "value"})):
            result = ai_lashing_condition(wire_ropes_with_findings(), "Wire Ropes")
        assert result == FALLBACK

    def test_passes_correct_max_tokens(self):
        with patch(PATCH, return_value=json.dumps(["Obs."])) as mock_pm:
            ai_lashing_condition(wire_ropes_with_findings(), "Wire Ropes")
        assert mock_pm.call_args.kwargs["max_tokens"] == 1200

    def test_strips_markdown_code_fence(self):
        observations = ["Kinks observed in wire rope."]
        raw = f"```json\n{json.dumps(observations)}\n```"
        with patch(PATCH, return_value=raw):
            result = ai_lashing_condition(wire_ropes_with_findings(), "Wire Ropes")
        assert result == observations


class TestAiLashingConditionShackles:

    def test_no_negative_findings_returns_early(self):
        with patch(PATCH) as mock_pm:
            result = ai_lashing_condition(shackles_all_pass(), "Shackles")
        assert result == NO_FINDINGS
        mock_pm.assert_not_called()

    def test_valid_response_returned(self):
        observations = ["Cracks detected on shackle body."]
        with patch(PATCH, return_value=json.dumps(observations)):
            result = ai_lashing_condition(shackles_with_findings(), "Shackles")
        assert result == observations

    def test_api_exception_returns_fallback(self):
        with patch(PATCH, side_effect=Exception("timeout")):
            result = ai_lashing_condition(shackles_with_findings(), "Shackles")
        assert result == FALLBACK


class TestAiLashingConditionOtherTypes:

    @pytest.mark.parametrize("lashing_type", [
        "Tensioner, turnbuckle, arm lever",
        "Stopper, dog plate",
        "Chain",
        "Synthetic Lines",
    ])
    def test_supported_types_call_prompt_model(self, lashing_type):
        observations = ["Finding noted."]
        with patch(PATCH, return_value=json.dumps(observations)) as mock_pm:
            # Provide a minimal failing field common to all types
            result = ai_lashing_condition({"lashing_plan": "No"}, lashing_type)
        mock_pm.assert_called_once()
        assert result == observations

    def test_unsupported_type_returns_error_message(self):
        with patch(PATCH) as mock_pm:
            result = ai_lashing_condition({"lashing_plan": "No"}, "Unknown Type")
        assert result == ["Unsupported lashing type."]
        mock_pm.assert_not_called()
