from importlib.metadata import version

from .core import (
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
    Bytes,
    String,
    Option,
)
from .enum import Enum

__version__ = version(__name__)
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
]
