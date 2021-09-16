from importlib.metadata import version

from .core import F32, F64, I8, I16, I32, I64, I128, U8, U16, U32, U64, U128, Bool

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
]
