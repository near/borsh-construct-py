# Defining New Types

You can build new schemas on top of `borsh-construct` using [`construct.Adapter`](https://construct.readthedocs.io/en/latest/adapters.html#adapting).

For example, here we implement (de)serialization for Python's `Fraction` class:

```python
from typing import Tuple
from fractions import Fraction
from construct import Adapter
from borsh_construct import I32, TupleStruct


class Frac(Adapter):
    def __init__(self, int_type) -> None:
        super().__init__(TupleStruct(int_type, int_type))  # type: ignore

    def _encode(self, obj: Fraction, context, path) -> Tuple[int, int]:
        return obj.numerator, obj.denominator

    def _decode(self, obj: Tuple[int, int], context, path) -> Fraction:
        numerator, denominator = obj
        return Fraction(numerator, denominator)

frac = Frac(I32)
to_serialize = Fraction(10, 3)
assert frac.parse(frac.build(to_serialize)) == to_serialize

```
