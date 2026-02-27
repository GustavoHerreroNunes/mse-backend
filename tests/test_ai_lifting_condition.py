import json
from unittest.mock import patch

import pytest

from reportlab_pages.utils.ai_lifting_condition import ai_lifting_condition

PATCH = "reportlab_pages.utils.ai_lifting_condition.prompt_model"
FALLBACK = ["Overall, the lifting material was determined to be in satisfactory operational condition."]
NO_FINDINGS = ["No negative findings observed."]


# --- Data helpers ---

def wire_ropes_all_pass():
    """All Wire Ropes fields considered passing — no findings expected."""
    return {
        "rigging_plan": "Yes",
        "rigging_items": "Yes",
        "rigging_material": "Yes",
        "rigging_condition": "Yes",
        "conclusion_wires_suitable": "Yes",
        "rigging_wires_acceptance": "Yes",
        "broken_wires": "No",
        "corrosion_wires_visible": "No",
    }

def wire_ropes_with_findings():
    return {
        "rigging_plan": "No",       # positive field → flagged when != Yes
        "broken_wires": "Yes",      # non-positive → flagged when == Yes
    }

def shackles_with_findings():
    return {
        "rigging_plan": "No",
        "fractures": "Yes",
    }

def hook_all_pass():
    return {
        "rigging_plan": "Yes",
        "rigging_items": "Yes",
        "rigging_material": "Yes",
        "rigging_condition": "Yes",
        "visible_mark": "Yes",
        "marked_limit": "Yes",
        "hook_type": "Yes",
        "throat_limits": "Yes",
        "hook_shape": "Yes",
        "intact_latch": "Yes",
        "correctly_latch": "Yes",
        "tension_latch": "Yes",
        "hook_rotation": "Yes",
        "locking_mechanism": "Yes",
        "smooth_joints": "Yes",
        "automatic_latch": "Yes",
        "hook_dimensions": "Yes",
        "throat_opening": "Yes",
        "rigging_hook_acceptance": "Yes",
        "cracks": "No",
        "dents": "No",
        "excessive_corrosion": "No",
    }

def hook_with_findings():
    return {
        "rigging_plan": "No",
        "cracks": "Yes",
    }


class TestAiLiftingConditionWireRopes:

    def test_no_negative_findings_returns_early(self):
        with patch(PATCH) as mock_pm:
            result = ai_lifting_condition(wire_ropes_all_pass(), "Wire Ropes")
        assert result == NO_FINDINGS
        mock_pm.assert_not_called()

    def test_does_not_apply_treated_as_passing(self):
        data = {**wire_ropes_all_pass(), "rigging_plan": "Does Not Apply"}
        with patch(PATCH) as mock_pm:
            result = ai_lifting_condition(data, "Wire Ropes")
        assert result == NO_FINDINGS
        mock_pm.assert_not_called()

    def test_valid_response_returned(self):
        observations = ["Wire rope shows internal corrosion.", "Rigging plan not followed."]
        with patch(PATCH, return_value=json.dumps(observations)):
            result = ai_lifting_condition(wire_ropes_with_findings(), "Wire Ropes")
        assert result == observations

    def test_api_exception_returns_fallback(self):
        with patch(PATCH, side_effect=RuntimeError("API error")):
            result = ai_lifting_condition(wire_ropes_with_findings(), "Wire Ropes")
        assert result == FALLBACK

    def test_invalid_json_returns_fallback(self):
        with patch(PATCH, return_value="invalid json"):
            result = ai_lifting_condition(wire_ropes_with_findings(), "Wire Ropes")
        assert result == FALLBACK

    def test_wrong_format_returns_fallback(self):
        with patch(PATCH, return_value=json.dumps({"key": "val"})):
            result = ai_lifting_condition(wire_ropes_with_findings(), "Wire Ropes")
        assert result == FALLBACK

    def test_passes_correct_max_tokens(self):
        with patch(PATCH, return_value=json.dumps(["Obs."])) as mock_pm:
            ai_lifting_condition(wire_ropes_with_findings(), "Wire Ropes")
        assert mock_pm.call_args.kwargs["max_tokens"] == 1200

    def test_strips_markdown_code_fence(self):
        observations = ["Bird caging deformation observed."]
        raw = f"```json\n{json.dumps(observations)}\n```"
        with patch(PATCH, return_value=raw):
            result = ai_lifting_condition(wire_ropes_with_findings(), "Wire Ropes")
        assert result == observations


class TestAiLiftingConditionHook:

    def test_no_negative_findings_returns_early(self):
        with patch(PATCH) as mock_pm:
            result = ai_lifting_condition(hook_all_pass(), "Hook")
        assert result == NO_FINDINGS
        mock_pm.assert_not_called()

    def test_valid_response_returned(self):
        observations = ["Hook shows visible deformation."]
        with patch(PATCH, return_value=json.dumps(observations)):
            result = ai_lifting_condition(hook_with_findings(), "Hook")
        assert result == observations

    def test_api_exception_returns_fallback(self):
        with patch(PATCH, side_effect=Exception("timeout")):
            result = ai_lifting_condition(hook_with_findings(), "Hook")
        assert result == FALLBACK


class TestAiLiftingConditionOtherTypes:

    @pytest.mark.parametrize("lifting_type", [
        "Shackles",
        "Master Link",
        "Chain",
        "Spreader",
        "Synthetic Sling",
    ])
    def test_supported_types_call_prompt_model(self, lifting_type):
        observations = ["Finding noted."]
        with patch(PATCH, return_value=json.dumps(observations)) as mock_pm:
            result = ai_lifting_condition({"rigging_plan": "No"}, lifting_type)
        mock_pm.assert_called_once()
        assert result == observations

    def test_unsupported_type_returns_error_message(self):
        with patch(PATCH) as mock_pm:
            result = ai_lifting_condition({"rigging_plan": "No"}, "Unknown Gear")
        assert result == ["Unsupported lifting type."]
        mock_pm.assert_not_called()
