from dataclasses import dataclass
import borsh


@dataclass
class ExampleStruct:
    """
    Primitive structure from borsh example
    """
    x: borsh.types.U64
    y: borsh.types.String


def test_serialize_with_dataclasses():

    obj_to_serialize = ExampleStruct(
        x=borsh.types.U64(3301),
        y=borsh.types.String("liber primus"),
    )
    serialized_bytes = borsh.serialize(obj_to_serialize)
    serialized = [x for x in serialized_bytes]

    assert serialized == [229, 12, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 108, 105, 98, 101, 114, 32, 112, 114, 105, 109, 117, 115]


def test_serialize_example_struct_with_none_value():
    obj_to_serialize = ExampleStruct(
        x=borsh.types.U64(3301),
        y=borsh.types.String(None),
    )

    serialized_bytes = borsh.serialize(obj_to_serialize)
    serialized = [x for x in serialized_bytes]

    assert serialized == [229, 12, 0, 0, 0, 0, 0, 0, 0]
