"""Core tests."""
from typing import Any

import pytest
from borsh import (
    F32,
    F64,
    I8,
    I16,
    I32,
    I64,
    I128,
    U8,
    U16,
    U32,
    U64,
    U128,
    Bool,
    Vec,
    CStruct,
    TupleStruct,
    Enum,
    String,
    Option,
)
from borsh.core import (
    NAMED_TUPLE_FIELD_ERROR,
    TUPLE_DATA,
    UNNAMED_SUBCON_ERROR,
    NON_STR_NAME_ERROR,
    UNDERSCORE_NAME_ERROR,
    TUPLE_DATA_NAME_ERROR,
)
from construct import Construct, Float32l, Float64l, FormatField, FormatFieldError

ENUM = Enum(
    "Unit",
    "TupleVariant" / TupleStruct(U128, String, I64, Option(U16)),
    "CStructVariant"
    / CStruct("u128_field" / U128, "string_field" / String, "vec_field" / Vec(U16)),
)

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
    (I16[3], [1, 2, 3], [1, 0, 2, 0, 3, 0]),
    (Vec(I16), [1, 1], [2, 0, 0, 0, 1, 0, 1, 0]),
    (
        TupleStruct(U128, String, I64, Option(U16)),
        [123, "hello", 1400, 13],
        [
            123,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            5,
            0,
            0,
            0,
            104,
            101,
            108,
            108,
            111,
            120,
            5,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            13,
            0,
        ],
    ),
    (
        CStruct("u128_field" / U128, "string_field" / String, "vec_field" / Vec(U16)),
        {"u128_field": 1033, "string_field": "hello", "vec_field": [1, 2, 3]},
        [
            9,
            4,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            5,
            0,
            0,
            0,
            104,
            101,
            108,
            108,
            111,
            3,
            0,
            0,
            0,
            1,
            0,
            2,
            0,
            3,
            0,
        ],
    ),
    (ENUM, ENUM.enum.Unit(), [0]),
    (
        ENUM,
        ENUM.enum.TupleVariant([10, "hello", 13, 12]),
        [
            1,
            10,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            5,
            0,
            0,
            0,
            104,
            101,
            108,
            108,
            111,
            13,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            12,
            0,
        ],
    ),
    (
        ENUM,
        ENUM.enum.CStructVariant(
            u128_field=15,
            string_field="hi",
            vec_field=[3, 2, 1],
        ),
        [
            2,
            15,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            104,
            105,
            3,
            0,
            0,
            0,
            3,
            0,
            2,
            0,
            1,
            0,
        ],
    ),
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


def test_named_tuple_struct_field_raises() -> None:
    with pytest.raises(ValueError) as exc:
        TupleStruct("foo" / U8)
    assert exc.value == NAMED_TUPLE_FIELD_ERROR


def test_unnamed_subcon_raises() -> None:
    """Check that error is raised when enum variant or CStruct field is unnamed."""
    with pytest.raises(ValueError) as excinfo:
        Enum("foo", TupleStruct(U8))
    assert str(excinfo.value) == str(UNNAMED_SUBCON_ERROR)


def test_non_str_name_raises() -> None:
    """Check that error is raised when subcon name is not a string."""
    with pytest.raises(ValueError) as excinfo:
        CStruct(1 / U8)
    assert str(excinfo.value) == str(NON_STR_NAME_ERROR)


def test_tuple_data_name_raises() -> None:
    """Check that error is raised when subcon name is not a string."""
    with pytest.raises(ValueError) as excinfo:
        CStruct(TUPLE_DATA / U8)
    assert str(excinfo.value) == str(TUPLE_DATA_NAME_ERROR)


def test_underscore_name_raises() -> None:
    """Check that error is raised when subcon name starts with underscore."""
    with pytest.raises(ValueError) as excinfo:
        CStruct("_foo" / U8)
    assert str(excinfo.value) == str(UNDERSCORE_NAME_ERROR)


def test_unrecognized_variant_type_raises() -> None:
    """Check that error is raised if variant type is not valid."""
    with pytest.raises(ValueError) as excinfo:
        Enum("foo" / U8)
    assert "Unrecognized" in str(excinfo.value)
