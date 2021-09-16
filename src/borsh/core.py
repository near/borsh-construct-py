from math import isnan

from construct import Adapter, Array, BytesInteger, Construct, Switch
from construct import singleton  # type: ignore
from construct import Flag as Bool
from construct import FormatField, FormatFieldError, GreedyBytes, IfThenElse
from construct import Int8sl as I8
from construct import Int8ul as U8
from construct import Int16sl as I16
from construct import Int16ul as U16
from construct import Int32sl as I32
from construct import Int32ul as U32
from construct import Int64sl as I64
from construct import Int64ul as U64
from construct import Pass, Prefixed, PrefixedArray, Renamed
from construct import Sequence as TupleStruct
from construct import Struct as CStruct

U128 = BytesInteger(16, signed=False, swapped=True)
I128 = BytesInteger(16, signed=True, swapped=True)


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
