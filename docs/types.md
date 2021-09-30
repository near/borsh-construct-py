This is an outline of all the types supported by `borsh-construct`. Since Borsh is Rust-centric, some Rust snippets are included to make it clear what the equivalent Rust type is.

## Numeric types

All numeric types mentioned in the Borsh spec are supported:

- Unsigned integers: U8, U16, U32, U64, U128
- Signed integers: I8, I16, I32, I64, I128
- Floats: F32, F64
- Bool (this is not explicitly part of the spec, but `borsh-rs` implements Bool as a `u8` with value 0 or 1)

Example:

```python
>>> from borsh_construct import U32
>>> U32.build(42)
b'*\x00\x00\x00'
>>> U32.parse(b'*\x00\x00\x00')
42

```


!!! note

    Most of the numeric types come directly from the `construct` library, and are just aliased so that they match the Borsh spec. For example, `borsh_construct.U8` is really `construct.Int8ul`.

## Fixed sized arrays

`construct` gives us a nice `[]` syntax to represent fixed sized arrays. For example, an array of 3 u8 integers:

```python
>>> from borsh_construct import U8
>>> U8[3].build([1, 2, 3])
b'\x01\x02\x03'
>>> U8[3].parse(b'\x01\x02\x03')
ListContainer([1, 2, 3])

```

This is what that fixed size array looks like in Rust:

```rust
let arr = [1u8, 2, 3];

```

## Dynamic sized arrays

Dynamic arrays are implemented using the `Vec` function:

```python
>>> from borsh_construct import Vec, U8
>>> Vec(U8).build([1, 2, 3])
b'\x03\x00\x00\x00\x01\x02\x03'
>>> Vec(U8).parse(b'\x03\x00\x00\x00\x01\x02\x03')
ListContainer([1, 2, 3])

```

In Rust we could build that vector like this:

```rust
let v = vec![1u8, 2, 3];

```

## C-like structs

This is analogous to a Rust struct with named fields:

```python
>>> from borsh_construct import CStruct, String, U8
>>> person = CStruct(
...     "name" / String,
...     "age" / U8
... )
>>> person.build({"name": "Alice", "age": 50})
b'\x05\x00\x00\x00Alice2'
>>> person.parse(b'\x05\x00\x00\x00Alice2')
Container(name=u'Alice', age=50)

```
Rust type:
```rust
struct Person {
    name: String,
    age: u8,
}

```

## Tuple structs
```python
>>> from borsh_construct import TupleStruct, I32, F32
>>> pair = TupleStruct(I32, F32)
>>> pair.build([3, 0.5])
b'\x03\x00\x00\x00\x00\x00\x00?'
>>> pair.parse(b'\x03\x00\x00\x00\x00\x00\x00?')
ListContainer([3, 0.5])

```
Rust type:
```rust
struct Pair(i32, f32);

```


## Enum

Rust's `enum` is the trickiest part of `borsh-construct` because it's rather different from Python's `enum.Enum`. Under the hood, `borsh-construct` uses the [`sumtypes`](https://sumtypes.readthedocs.io/en/latest/) library to represent Rust enums in Python.

Notice below how our `message` object has a `.enum` attribute: this is the Python imitation of Rust's enum type.

Defining an enum:

```python
>>> from borsh_construct import Enum, I32, CStruct, TupleStruct, String
>>> message = Enum(
...     "Quit",
...     "Move" / CStruct("x" / I32, "y" / I32),
...     "Write" / TupleStruct(String),
...     "ChangeColor" / TupleStruct(I32, I32, I32),
...     enum_name="Message",
... )
>>> message.build(message.enum.Quit())
b'\x00'
>>> message.parse(b'\x00')
Message.Quit()
>>> message.build(message.enum.Move(x=1, y=3))
b'\x01\x01\x00\x00\x00\x03\x00\x00\x00'
>>> message.parse(b'\x01\x01\x00\x00\x00\x03\x00\x00\x00')
Message.Move(x=1, y=3)
>>> message.build(message.enum.Write(("hello",)))
b'\x02\x05\x00\x00\x00hello'
>>> message.parse(b'\x02\x05\x00\x00\x00hello')
Message.Write(tuple_data=ListContainer(['hello']))
>>> message.build(message.enum.ChangeColor((1, 2, 3)))
b'\x03\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00'
>>> message.parse(b'\x03\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00')
Message.ChangeColor(tuple_data=ListContainer([1, 2, 3]))

```

Notice also how each variant of the enum is a subclass of the enum itself:

```python
>>> assert isinstance(message.enum.Quit(), message.enum)

```

Rust type:
```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
```

## HashMap

You can think of HashMap as a Python dictionary as long as the keys and values have a well-defined type.

```python
>>> from borsh_construct import HashMap, String, U32
>>> scores = HashMap(String, U32)
>>> scores.build({"Blue": 10, "Yellow": 50})
b'\x02\x00\x00\x00\x04\x00\x00\x00Blue\n\x00\x00\x00\x06\x00\x00\x00Yellow2\x00\x00\x00'
>>> scores.parse(b'\x02\x00\x00\x00\x04\x00\x00\x00Blue\n\x00\x00\x00\x06\x00\x00\x00Yellow2\x00\x00\x00')
{'Blue': 10, 'Yellow': 50}

```
Rust type:
```rust
fn main() {
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);
}
```

## HashSet

The HashSet is similar to a Python `set` with a well-defined type.

```python
>>> from borsh_construct import HashSet, I32
>>> a = HashSet(I32)
>>> a.build({1, 2, 3})
b'\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00'
>>> a.parse(b'\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00')
{1, 2, 3}

```
Rust type:
```rust
use std::collections::HashSet;

fn main() {
    let mut a: HashSet<i32> = vec![1i32, 2, 3].into_iter().collect();
}

```

## Option

Rust programmers will notice that our Option type is not implemented like a Rust enum, because it's not worth the complexity.

```python
>>> from borsh_construct import Option, U8
>>> optional_num = Option(U8)
>>> optional_num.build(None)
b'\x00'
>>> optional_num.parse(b'\x00') is None
True
>>> optional_num.build(3)
b'\x01\x03'
>>> optional_num.parse(b'\x01\x03')
3

```
Rust type:
```rust
Option<u8>
```

## Bytes

The Borsh spec doesn't specifically mention serializing raw bytes, but it's worth including anyway:

```python
>>> from borsh_construct import Bytes
>>> Bytes.build(bytes([1, 2, 3]))
b'\x03\x00\x00\x00\x01\x02\x03'
>>> Bytes.parse(b'\x03\x00\x00\x00\x01\x02\x03')
b'\x01\x02\x03'

```
Rust type:
```rust
vec![1u8, 2, 3]

```

## String

Python:

```python
>>> from borsh_construct import String
>>> String.build("🚀🚀🚀")
b'\x0c\x00\x00\x00\xf0\x9f\x9a\x80\xf0\x9f\x9a\x80\xf0\x9f\x9a\x80'
>>> String.parse(b'\x0c\x00\x00\x00\xf0\x9f\x9a\x80\xf0\x9f\x9a\x80\xf0\x9f\x9a\x80')
'🚀🚀🚀'

```

Rust type:

```rust
String::from("🚀🚀🚀")

```


