from importlib.metadata import version, PackageNotFoundError
from construct import Flag as Bool
from construct import Int8sl as I8
from construct import Int16sl as I16
from construct import Int16ul as U16
from construct import Int32sl as I32
from construct import Int64sl as I64
from construct import Int64ul as U64

from .core import (
    F32,
    F64,
    I128,
    U8,
    U32,
    U128,
    Vec,
    CStruct,
    TupleStruct,
    Bytes,
    String,
    Option,
    HashMap,
    HashSet,
)
from .enum import Enum

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

__all__ = [
    "I8",
    "I16",
    "I32",
    "U8",
    "I64",
    "I128",
    "U16",
    "U32",
    "U64",
    "U128",
    "F32",
    "F64",
    "Bool",
    "Vec",
    "CStruct",
    "TupleStruct",
    "Bytes",
    "String",
    "Enum",
    "Option",
    "HashMap",
    "HashSet",
]
