This is an outline of all the types supported by Borsh. Since Borsh is Rust-centric, some Rust snippets are included to make it clear what the equivalent Rust type is.

## Numeric types

All numeric types mentioned in the Borsh spec are supported:

- Unsigned integers: U8, U16, U32, U64, U128
- Signed integers: I8, I16, I32, I64, I128
- Floats: F32, F64
- Bool (this is not explicitly part of the spec, but `borsh-rs` implements Bool as a `u8` with value 0 or 1)

Example:

```python
>>> from borsh import U32
>>> U32.build(42)
b'*\x00\x00\x00'

```


!!! note

    Most of the numeric types come directly from the `construct` library, and are just aliased so that they match the Borsh spec. For example, `borsh.U8` is really `construct.Int8ul`.

## Fixed sized arrays

`construct` gives us a nice `[]` syntax to represent fixed sized arrays. For example, an array of 3 u8 integers:

```python
>>> from borsh import U8
>>> U8[3].build([1, 2, 3])
b'\x01\x02\x03'

```

This is what that fixed size array looks like in Rust:

```rust
let arr = [1u8, 2u8, 3u8];

```

## Dynamic sized arrays

Dynamic arrays are implemented using the `Vec` function:

```python
>>> from borsh import Vec, U8
>>> Vec(U8).build([1, 2, 3])
b'\x03\x00\x00\x00\x01\x02\x03'

```

In Rust we could build that vector like this:

```rust
let v = vec![1u8, 2, 3];

```

## C-like structs

This is analogous to a Rust struct with named fields:

```python
>>> from borsh import CStruct, String, U8
>>> person = CStruct(
...     "name" / String,
...     "age" / U8
... )
>>> person.build({"name": "Alice", "age": 50})
b'\x05\x00\x00\x00Alice2'

```
Rust type:
```rust
struct Person {
    name: String,
    age: u8,
}

```