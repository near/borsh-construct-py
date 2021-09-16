# borsh-py

`borsh-py` is an implementation of the Borsh binary serialization format for Python projects.

Borsh stands for Binary Object Representation Serializer for Hashing. It is meant to be used in security-critical projects as it prioritizes consistency, safety, speed, and comes with a strict specification.


### Setup

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Install dev dependencies:
```sh
poetry install
```
3. Install [nox-poetry](https://github.com/cjolowicz/nox-poetry)
4. Activate the poetry shell:
```sh
poetry shell
```

### Tests
```sh
nox
```
