"""Unit tests for grade_average.calculate_average.

Each test follows Arrange / Act / Assert (AAA). The Arrange step is the
input data supplied by @pytest.mark.parametrize.
"""
import pytest

from src.grade_average import calculate_average


# ---------- Valid inputs: correct average (spec 3.1) ----------
#
# DEFECT DEF-01 (found by TC-AVG-02, TC-AVG-06, TC-AVG-07)
#   Requirement: spec 3.1.1 - divide the sum by 2 using ordinary division
#                and keep any fractional part; do not round down.
#   Expected:    calculate_average(50, 51) returns 50.5
#   Actual:      calculate_average(50, 51) returns 50
#                (likewise 0, 1 -> 0 instead of 0.5; 99, 100 -> 99 instead of 99.5)
#   Cause:       src/grade_average.py, last line uses floor division:
#                    return (mark_one + mark_two) // 2
#                It should use ordinary division: (mark_one + mark_two) / 2
#   Note:        TC-AVG-01, 03, 04 and 05 pass only because their sums are even.

@pytest.mark.parametrize(
    "mark_one, mark_two, expected",
    [
        pytest.param(70, 80, 75, id="TC-AVG-01 even sum"),
        pytest.param(50, 51, 50.5, id="TC-AVG-02 odd sum keeps fraction"),
        pytest.param(0, 0, 0, id="TC-AVG-03 both lower boundary"),
        pytest.param(100, 100, 100, id="TC-AVG-04 both upper boundary"),
        pytest.param(0, 100, 50, id="TC-AVG-05 min and max"),
        pytest.param(0, 1, 0.5, id="TC-AVG-06 just above lower boundary"),
        pytest.param(99, 100, 99.5, id="TC-AVG-07 just below upper boundary"),
    ],
)
def test_calculate_average_returns_arithmetic_mean(mark_one, mark_two, expected):
    # Arrange: mark_one, mark_two and expected come from the parameters above
    # Act
    result = calculate_average(mark_one, mark_two)
    # Assert
    assert result == expected


# ---------- Correct type, out of range: ValueError (spec 2.4) ----------

@pytest.mark.parametrize(
    "mark_one, mark_two",
    [
        pytest.param(-1, 50, id="TC-AVG-08 mark_one below range"),
        pytest.param(50, -1, id="TC-AVG-09 mark_two below range"),
        pytest.param(101, 50, id="TC-AVG-10 mark_one above range"),
        pytest.param(50, 101, id="TC-AVG-11 mark_two above range"),
    ],
)
def test_calculate_average_out_of_range_raises_value_error(mark_one, mark_two):
    # Arrange: out-of-range marks come from the parameters above
    # Act and Assert: the call must raise ValueError
    with pytest.raises(ValueError):
        calculate_average(mark_one, mark_two)


# ---------- Wrong type: TypeError (spec 2.2, 2.3) ----------

@pytest.mark.parametrize(
    "mark_one, mark_two",
    [
        pytest.param(50.0, 50, id="TC-AVG-12 float"),
        pytest.param(50, "50", id="TC-AVG-13 string"),
        pytest.param(None, 50, id="TC-AVG-14 None"),
        pytest.param(True, 50, id="TC-AVG-15 bool True"),
        pytest.param(50, False, id="TC-AVG-16 bool False"),
    ],
)
def test_calculate_average_invalid_type_raises_type_error(mark_one, mark_two):
    # Arrange: invalid-type marks come from the parameters above
    # Act and Assert: the call must raise TypeError
    with pytest.raises(TypeError):
        calculate_average(mark_one, mark_two)
