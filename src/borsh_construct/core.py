from typing import Any, Optional, List, Tuple
from math import isnan
from construct import Adapter, Array, BytesInteger, Construct
from construct import singleton  # type: ignore
from construct import FormatField, FormatFieldError, GreedyBytes, IfThenElse
from construct import Int8ul as U8
from construct import Int32ul as U32
from construct import Pass, Prefixed, PrefixedArray
from construct import Sequence
from construct import Struct

TUPLE_DATA = "tuple_data"

NAMED_TUPLE_FIELD_ERROR = ValueError("TupleStruct cannot have named fields")
UNNAMED_SUBCON_ERROR = ValueError("CStruct fields and enum variants must be named")
NON_STR_NAME_ERROR = ValueError("Names must be strings.")
TUPLE_DATA_NAME_ERROR = ValueError(
    f"The name {TUPLE_DATA} is reserved. If you encountered this "
    "error it's either a wild coincidence or you're "
    "doing it wrong."  # noqa: C812
)
UNDERSCORE_NAME_ERROR = ValueError("names cannot start with an underscore.")
U128 = BytesInteger(16, signed=False, swapped=True)
I128 = BytesInteger(16, signed=True, swapped=True)


class TupleStruct(Sequence):
    """Python implementation of Rust tuple struct."""

    def __init__(self, *subcons) -> None:
        super().__init__(*subcons)  # type: ignore
        for subcon in self.subcons:
            if subcon.name is not None:
                raise NAMED_TUPLE_FIELD_ERROR


class CStruct(Struct):
    """Python implementation of Rust C-like struct."""

    def __init__(self, *subcons) -> None:
        super().__init__(*subcons)
        for subcon in subcons:
            check_subcon_name(subcon.name)


def _check_name_not_null(name: Optional[str]) -> None:
    if name is None:
        raise UNNAMED_SUBCON_ERROR


def check_subcon_name(name: Optional[str]) -> None:
    """Check that CStructs and Enums have valid names."""  # noqa: DAR101
    _check_name_not_null(name)
    if not isinstance(name, str):
        raise NON_STR_NAME_ERROR
    if name == TUPLE_DATA:
        raise TUPLE_DATA_NAME_ERROR
    if name[0] == "_":
        raise UNDERSCORE_NAME_ERROR


class FormatFieldNoNan(FormatField):
    """Adapted form of `construct.FormatField` that forbids nan."""

    def _parse(self, stream, context, path):
        result = super()._parse(stream, context, path)
        if isnan(result):
            raise FormatFieldError("Borsh does not support nan.")
        return result

    def _build(self, obj, stream, context, path):
        if isnan(obj):
            raise FormatFieldError("Borsh does not support nan.")
        return super()._build(obj, stream, context, path)


@singleton
def F32() -> FormatFieldNoNan:  # noqa: N802
    """Little endian, 32-bit IEEE floating point number."""
    return FormatFieldNoNan("<", "f")


@singleton
def F64() -> FormatFieldNoNan:  # noqa: N802
    """Little endian, 64-bit IEEE floating point number."""
    return FormatFieldNoNan("<", "d")


def Vec(subcon: Construct) -> Array:  # noqa: N802
    """Dynamic sized array.

    Args:
        subcon (Construct): the type of the array members.

    Returns:
        Array: a Construct PrefixedArray.
    """
    return PrefixedArray(U32, subcon)


Bytes = Prefixed(U32, GreedyBytes)


class _String(Adapter):
    def __init__(self) -> None:
        super().__init__(Bytes)  # type: ignore

    def _decode(self, obj: bytes, context, path) -> str:
        return obj.decode("utf8")

    def _encode(self, obj: str, context, path) -> bytes:
        return bytes(obj, "utf8")


String = _String()


class Option(Adapter):
    """Borsh implementation for Rust's Option type."""

    _discriminator_key = "discriminator"
    _value_key = "value"

    def __init__(self, subcon: Construct) -> None:
        option_struct = CStruct(
            self._discriminator_key / U8,
            self._value_key
            / IfThenElse(lambda this: this[self._discriminator_key] == 0, Pass, subcon),
        )
        super().__init__(option_struct)  # type: ignore

    def _decode(self, obj, context, path) -> Any:
        return obj[self._value_key]

    def _encode(self, obj, context, path) -> dict:
        discriminator = 0 if obj is None else 1
        return {self._discriminator_key: discriminator, self._value_key: obj}


class HashMap(Adapter):
    """Borsh implementation for Rust HashMap."""

    def __init__(self, key_subcon: Construct, value_subcon: Construct) -> None:
        super().__init__(
            PrefixedArray(U32, TupleStruct(key_subcon, value_subcon)),
        )  # type: ignore

    def _decode(self, obj: List[Tuple[Any, Any]], context, path) -> dict:
        return dict(obj)

    def _encode(self, obj, context, path) -> List[Tuple]:
        return sorted(obj.items())


class HashSet(Adapter):
    """Python implementation of Rust HashSet."""

    def __init__(self, subcon: Construct) -> None:
        super().__init__(PrefixedArray(U32, subcon))  # type: ignore

    def _decode(self, obj, context, path) -> set:
        return set(obj)

    def _encode(self, obj, context, path) -> list:
        return sorted(obj)
