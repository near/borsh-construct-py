"""Core tests."""
from typing import Any

import pytest
from borsh import F32, F64, I8, I16, I32, I64, I128, U8, U16, U32, U64, U128, Bool
from construct import Construct, Float32l, Float64l, FormatField, FormatFieldError

TYPE_INPUT_EXPECTED = (
    (Bool, True, [1]),
    (Bool, False, [0]),
    (U8, 255, [255]),
    (I8, -128, [128]),
    (U16, 65535, [255, 255]),
    (I16, -32768, [0, 128]),
    (U32, 4294967295, [255, 255, 255, 255]),
    (I32, -2147483648, [0, 0, 0, 128]),
    (U64, 18446744073709551615, [255, 255, 255, 255, 255, 255, 255, 255]),
    (I64, -9223372036854775808, [0, 0, 0, 0, 0, 0, 0, 128]),
    (
        U128,
        340282366920938463463374607431768211455,
        [
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
            255,
        ],
    ),
    (
        I128,
        -170141183460469231731687303715884105728,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128],
    ),
    (F32, 0.5, [0, 0, 0, 63]),
    (F64, -0.5, [0, 0, 0, 0, 0, 0, 224, 191]),
)


@pytest.mark.parametrize("obj_type,obj_input,expected", TYPE_INPUT_EXPECTED)
def test_serde(obj_type: Construct, obj_input: Any, expected: Any) -> None:
    """Tests that inputs are serialized and deserialized as expected."""
    serialized = obj_type.build(obj_input)
    assert list(serialized) == expected
    deserialized = obj_type.parse(serialized)
    assert deserialized == obj_input


@pytest.mark.parametrize(
    "nonan_type,construct_type",
    [(F32, Float32l), (F64, Float64l)],
)
def test_nan_floats(nonan_type: FormatField, construct_type: FormatField) -> None:
    """Check that error is raised if you try to build or parse nan floats."""
    nan = float("nan")  # noqa: WPS456
    with pytest.raises(FormatFieldError):
        nonan_type.build(nan)
    nan_serialized = construct_type.build(nan)
    with pytest.raises(FormatFieldError):
        nonan_type.parse(nan_serialized)
