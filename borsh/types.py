"""
Standard types
"""
from dataclasses import dataclass

class BaseTypeMixin:

    def _serialize(self, value, n_bytes) -> bytearray:
        """
        Common serialization method
        """
        array = bytearray()
        assert value >= 0, "Can't serialize negative numbers %d" % value
        for i in range(n_bytes):
            array.append(value & 255)
            value //= 256
        assert value == 0, "Value %d has more that %d bytes" % (self.value, n_bytes)
        return array

    def serialize(self) -> bytearray:
        if self.value is not None:
            return self._serialize(self.value, self._size)
        # In case of None
        return self._serialize(value=0, n_bytes=1)


@dataclass
class U64(BaseTypeMixin):
    """
    Class to store unsigned 64 bytes integer
    """
    value: int
    _size: int = 64 // 8


@dataclass
class String(BaseTypeMixin):
    """
    Class to store String
    """
    value: str
    _size: int = 4

    def serialize(self) -> bytearray:
        if self.value is None:
            return super()._serialize(value=0, n_bytes=1)
        encoded_value = self.value.encode('utf8')
        return super()._serialize(len(encoded_value), self._size) + encoded_value

