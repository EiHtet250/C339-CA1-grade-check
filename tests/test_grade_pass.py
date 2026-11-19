"""Unit tests for grade_pass.has_passed.

Each test case has an ID (TC-PASS-xx) that is shown in the pytest -v output.
"""
import pytest

from grade_pass import has_passed


# ---------- Valid inputs: pass / not pass (spec 3.2) ----------

@pytest.mark.parametrize(
    "score, expected",
    [
        pytest.param(0, False, id="TC-PASS-01 lower boundary"),
        pytest.param(1, False, id="TC-PASS-02 just above lower boundary"),
        pytest.param(49, False, id="TC-PASS-03 just below pass mark"),
        pytest.param(50, True, id="TC-PASS-04 exactly pass mark"),
        pytest.param(51, True, id="TC-PASS-05 just above pass mark"),
        pytest.param(99, True, id="TC-PASS-06 just below upper boundary"),
        pytest.param(100, True, id="TC-PASS-07 upper boundary"),
    ],
)
def test_has_passed_returns_expected_status(score, expected):
    assert has_passed(score) is expected



# ---------- Correct type, out of range: ValueError (spec 2.4) ----------

@pytest.mark.parametrize(
    "score",
    [
        pytest.param(-1, id="TC-PASS-09 below range"),
        pytest.param(101, id="TC-PASS-10 above range"),
    ],
)
def test_has_passed_out_of_range_raises_value_error(score):
    with pytest.raises(ValueError):
        has_passed(score)


# ---------- Wrong type: TypeError (spec 2.2, 2.3, 3.2.2) ----------

@pytest.mark.parametrize(
    "score",
    [
        pytest.param(50.0, id="TC-PASS-11 float"),
        pytest.param("50", id="TC-PASS-12 string"),
        pytest.param(None, id="TC-PASS-13 None"),
        pytest.param(True, id="TC-PASS-14 bool True"),
        pytest.param(False, id="TC-PASS-15 bool False"),
    ],
)
def test_has_passed_invalid_type_raises_type_error(score):
    with pytest.raises(TypeError):
        has_passed(score)
