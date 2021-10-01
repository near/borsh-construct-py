from hypothesis import given
import hypothesis.strategies as st

from borsh_construct import (
    U8,
    I8,
    U16,
    I16,
    U32,
    I32,
    U64,
    I64,
    U128,
    I128,
    F32,
    F64,
    String,
    Bytes,
    HashMap,
    HashSet,
    Vec,
    Option,
)


borsh_simple_types = (
    U8,
    I8,
    U16,
    I16,
    U32,
    I32,
    U64,
    I64,
    U128,
    I128,
    F32,
    F64,
    Bytes,
    String,
)
borsh_compound_types = (
    HashMap,
    HashSet,
    Vec,
    Option,
)


@given(st.text())
def test_string(s):
    """Test string encoding/decoding."""
    assert String.parse(String.build(s)) == s


u8_ints = st.integers(0, 255)
i8_ints = st.integers(-128, 127)
u16_ints = st.integers(0, 65535)
i16_ints = st.integers(-32768, 32767)
u32_ints = st.integers(0, 4294967295)
i32_ints = st.integers(-2147483648, 2147483647)
u64_ints = st.integers(0, 18446744073709551615)
i64_ints = st.integers(-9223372036854775808, 9223372036854775807)
u128_ints = st.integers(0, 340282366920938463463374607431768211455)
i128_ints = st.integers(
    -170141183460469231731687303715884105728,
    170141183460469231731687303715884105727,
)
f32_floats = st.floats(width=32, allow_nan=False)
f64_floats = st.floats(width=64, allow_nan=False)
numeric_strategies = (
    u8_ints,
    i8_ints,
    u16_ints,
    i16_ints,
    u32_ints,
    i32_ints,
    u64_ints,
    i64_ints,
    u128_ints,
    i128_ints,
)

type_map = {
    U8: u8_ints,
    I8: i8_ints,
    U16: u16_ints,
    I16: i16_ints,
    U32: u32_ints,
    I32: i32_ints,
    U64: u64_ints,
    I64: i64_ints,
    U128: u128_ints,
    I128: i128_ints,
    F32: f32_floats,
    F64: f64_floats,
    Bytes: st.binary(),
    String: st.text(),
}


@given(u8_ints)
def test_u8(s):
    """Test U8 encoding/decoding."""
    assert U8.parse(U8.build(s)) == s


@given(i8_ints)
def test_i8(s):
    """Test I8 encoding/decoding."""
    assert I8.parse(I8.build(s)) == s


@given(u16_ints)
def test_u16(s):
    """Test I16 encoding/decoding."""
    assert U16.parse(U16.build(s)) == s


@given(i16_ints)
def test_i16(s):
    """Test I16 encoding/decoding."""
    assert I16.parse(I16.build(s)) == s


@given(u32_ints)
def test_u32(s):
    """Test U32 encoding/decoding."""
    assert U32.parse(U32.build(s)) == s


@given(i32_ints)
def test_i32(s):
    """Test I32 encoding/decoding."""
    assert I32.parse(I32.build(s)) == s


@given(u64_ints)
def test_u64(s):
    """Test U64 encoding/decoding."""
    assert U64.parse(U64.build(s)) == s


@given(i64_ints)
def test_i64(s):
    """Test I64 encoding/decoding."""
    assert I64.parse(I64.build(s)) == s


@given(u128_ints)
def test_u128(s):
    """Test U128 encoding/decoding."""
    assert U128.parse(U128.build(s)) == s


@given(i128_ints)
def test_i128(s):
    """Test I128 encoding/decoding."""
    assert I128.parse(I128.build(s)) == s


@given(f32_floats)
def test_f32(s):
    """Test F32 encoding/decoding."""
    assert F32.parse(F32.build(s)) == s


@given(f64_floats)
def test_f64(s):
    """Test F64 encoding/decoding."""
    assert F64.parse(F64.build(s)) == s


@st.composite
def element_and_borsh_type(draw, elements=st.sampled_from(borsh_simple_types)):
    """Return a simple borsh type and a simple example of data fitting that type."""
    borsh_type = draw(elements)
    data_strategy = type_map[borsh_type]
    data = draw(data_strategy)
    return data, borsh_type


@st.composite
def list_data_and_borsh_type(
    draw,
    elements=st.sampled_from(borsh_simple_types),
    min_length=0,
    unique=False,
):
    """Return a list whose elements fit a particular borsh type."""
    borsh_type = draw(elements)
    data_strategy = type_map[borsh_type]
    data = draw(st.lists(data_strategy, min_size=min_length, unique=unique))
    return data, borsh_type, len(data)


@given(list_data_and_borsh_type())  # type: ignore
def test_vec(data_borsh_type):
    """Test Vec encoding."""
    data, borsh_type, _ = data_borsh_type
    vec_type = Vec(borsh_type)
    assert vec_type.parse(vec_type.build(data)) == data


@given(list_data_and_borsh_type(min_length=1))  # type: ignore
def test_array(data_borsh_type):
    """Test Array encoding."""
    data, borsh_type, length = data_borsh_type
    array_type = borsh_type[length]
    assert array_type.parse(array_type.build(data)) == data


@given(element_and_borsh_type())  # type: ignore
def test_option(data_borsh_type):
    """Test Option encoding."""
    data, borsh_type = data_borsh_type
    option_type = Option(borsh_type)
    assert option_type.parse(option_type.build(data)) == data


@given(list_data_and_borsh_type())  # type: ignore
def test_hashset(data_borsh_type):
    """Test HashSet encoding."""
    data, borsh_type, _ = data_borsh_type
    data = set(data)
    set_type = HashSet(borsh_type)
    assert set_type.parse(set_type.build(data)) == data
