"""Unit tests for grade_pass.has_passed.

Each test follows Arrange / Act / Assert (AAA). The Arrange step is the
input data supplied by @pytest.mark.parametrize.
"""
import pytest

from src.grade_pass import has_passed


# ---------- Valid inputs: pass / not pass (spec 3.2) ----------
#
# DEFECT DEF-02 (found by TC-PASS-04)
#   Requirement: spec 3.2.1 - a score of 50 or more is a pass.
#   Expected:    has_passed(50) returns True
#   Actual:      has_passed(50) returns False
#   Cause:       src/grade_pass.py, last line uses the wrong comparison:
#                    return score > 50
#                It should include the pass mark: return score >= 50
#   Note:        TC-PASS-03 (49) and TC-PASS-05 (51) pass, so only the exact
#                boundary value 50 exposes this defect.

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
    # Arrange: score and expected come from the parameters above
    # Act
    result = has_passed(score)
    # Assert: "is" also checks the result is a real bool (spec 3.2 Output)
    assert result is expected


# ---------- Correct type, out of range: ValueError (spec 2.4) ----------

@pytest.mark.parametrize(
    "score",
    [
        pytest.param(-1, id="TC-PASS-08 below range"),
        pytest.param(101, id="TC-PASS-09 above range"),
    ],
)
def test_has_passed_out_of_range_raises_value_error(score):
    # Arrange: out-of-range score comes from the parameters above
    # Act and Assert: the call must raise ValueError
    with pytest.raises(ValueError):
        has_passed(score)


# ---------- Wrong type: TypeError (spec 2.2, 2.3, 3.2.2) ----------

@pytest.mark.parametrize(
    "score",
    [
        pytest.param(50.0, id="TC-PASS-10 float"),
        pytest.param("50", id="TC-PASS-11 string"),
        pytest.param(None, id="TC-PASS-12 None"),
        pytest.param(True, id="TC-PASS-13 bool True"),
        pytest.param(False, id="TC-PASS-14 bool False"),
    ],
)
def test_has_passed_invalid_type_raises_type_error(score):
    # Arrange: invalid-type score comes from the parameters above
    # Act and Assert: the call must raise TypeError
    with pytest.raises(TypeError):
        has_passed(score)
