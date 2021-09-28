# Introduction

`borsh-py` is an implementation of the [Borsh](https://borsh.io/) binary serialization format for Python projects.

Borsh stands for Binary Object Representation Serializer for Hashing. It is meant to be used in security-critical projects as it prioritizes consistency, safety, speed, and comes with a strict specification.

`borsh-py` is built on top of the very powerful [`construct`](https://construct.readthedocs.io/en/latest/) library, so it is strongly recommended that you have a look at the basics of `construct` before using `borsh-py`.

## Who is this for?

This library was built with the NEAR and Solana blockchains in mind: the only obvious reason to use `borsh-py` currently is to write client code for those blockchains, as they typically expect Borsh serialization.

You may find other reasons to use `borsh-py`, but it is worth noting that the Borsh spec is written from a Rust perspective, so if you're not interacting with a Rust project then Borsh may not make sense.

## Installation

`pip install borsh`

Alternatively, using conda/mamba:

`mamba install borsh -c conda-forge`

## Usage

Since `borsh-py` is built with `construct`, it serializes objects using `.build` and deserializes them using `.parse`. For example:

```python
>>> from borsh import U8, String, CStruct
>>> animal = CStruct(
...     "name" / String,
...     "legs" / U8
... )
>>> animal.build({"name": "Ferris", "legs": 6})
b'\x06\x00\x00\x00Ferris\x06'
>>> animal.parse(b'\x06\x00\x00\x00Ferris\x06')
Container(name=u'Ferris', legs=6)

```
