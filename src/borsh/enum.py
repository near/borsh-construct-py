from typing import List, cast, Any, Dict
from sumtypes import sumtype, constructor
from construct import Pass, Renamed, Adapter, Switch, Container
import attr

from .core import CStruct, TupleStruct, U8, TUPLE_DATA, check_subcon_name


def _rust_enum(klass):
    indexed = sumtype(klass)
    for idx, cname in enumerate(indexed._sumtype_constructor_names):  # noqa: WPS437
        constructr = getattr(indexed, cname)
        constructr.index = idx

    # __getitem__ magic method cannot be classmethod
    @classmethod
    def getitem(cls, _index: int):  # noqa: WPS614
        return getattr(cls, cls._sumtype_constructor_names[_index])

    indexed.getitem = getitem

    return indexed


def _tuple_struct():
    return constructor(**{TUPLE_DATA: attr.ib(type=tuple)})


def _unit_struct():
    return constructor()


def _clike_struct(*fields: str):
    return constructor(*fields)


def _handle_cstruct_variant(underlying_variant, variant_name, enum_def) -> None:
    subcon_names: List[str] = []
    for s in underlying_variant.subcons:
        name = s.name
        subcon_names.append(cast(str, name))
    setattr(enum_def, variant_name, _clike_struct(*subcon_names))


def _handle_struct_variant(variant, enum_def) -> None:
    variant_name = variant.name
    check_subcon_name(variant_name)
    underlying_variant = variant.subcon if isinstance(variant, Renamed) else variant
    if isinstance(underlying_variant, TupleStruct):
        setattr(enum_def, variant_name, _tuple_struct())
    elif isinstance(underlying_variant, CStruct):
        _handle_cstruct_variant(underlying_variant, variant_name, enum_def)
    else:
        variant_type = type(underlying_variant)
        raise ValueError(f"Unrecognized variant type: {variant_type}")


def _make_enum(*variants):
    class EnumDef:  # noqa: WPS431
        """Python representation of Rust's Enum type."""

    for variant in variants:
        if isinstance(variant, str):
            setattr(EnumDef, variant, _unit_struct())
        else:
            _handle_struct_variant(variant, EnumDef)

    return _rust_enum(EnumDef)


class Enum(Adapter):
    """Borsh representation of Rust's enum type."""

    _index_key = "index"
    _value_key = "value"

    def __init__(self, *variants) -> None:
        """Borsh representation of Rust's enum type."""  # noqa: DAR101
        self.enum = _make_enum(*variants)
        self.variants = variants
        switch_cases = {}
        for idx, var in enumerate(variants):
            if isinstance(var, str):
                parser = Pass
            else:
                parser = var
            switch_cases[idx] = parser
        enum_struct = CStruct(
            self._index_key / U8,
            self._value_key / Switch(lambda this: this.index, switch_cases),
        )
        super().__init__(enum_struct)  # type: ignore

    def _decode(self, obj: Any, context, path) -> Any:
        index = obj.index
        enum_variant = self.enum.getitem(index)
        val = obj.value  # WPS421
        if val is None:
            return enum_variant()
        if isinstance(val, Container):
            return enum_variant(**{k: v for k, v in val.items() if k != "_io"})
        return enum_variant(val)

    def _encode(self, obj: Any, context, path) -> Dict[str, Any]:
        index = obj.index
        as_dict = attr.asdict(obj)
        if as_dict:
            try:
                to_build = as_dict[TUPLE_DATA]
            except KeyError:
                to_build = as_dict
        else:
            to_build = None
        return {self._index_key: index, self._value_key: to_build}
