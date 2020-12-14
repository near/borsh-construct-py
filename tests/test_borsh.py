from collections import namedtuple
import borsh

A = namedtuple('A', ['x', 'y'])


def test_serialize():
    obj_to_serialize = A(x=3301, y="liber primus")
    assert borsh.serialize(obj_to_serialize) == [229, 12, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 108, 105, 98, 101, 114, 32, 112, 114, 105, 109, 117, 115]
