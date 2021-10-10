# borsh-construct

[![Tests](https://github.com/near/borsh-construct-py/workflows/Tests/badge.svg)](https://github.com/near/borsh-construct-py/actions?workflow=Tests)
[![Docs](https://github.com/near/borsh-construct-pye/workflows/Docs/badge.svg)](https://near.github.io/borsh-construct-py/)

`borsh-construct` is an implementation of the [Borsh](https://borsh.io/) binary serialization format for Python projects.

Borsh stands for Binary Object Representation Serializer for Hashing. It is meant to be used in security-critical projects as it prioritizes consistency, safety, speed, and comes with a strict specification.

## Installation

```sh
pip install borsh-construct

```


### Development Setup

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Install dev dependencies:
```sh
poetry install

```
3. Install [nox-poetry](https://github.com/cjolowicz/nox-poetry) (note: do not use Poetry to install this, see [here](https://medium.com/@cjolowicz/nox-is-a-part-of-your-global-developer-environment-like-poetry-pre-commit-pyenv-or-pipx-1cdeba9198bd))
4. Activate the poetry shell:
```sh
poetry shell

```

### Quick Tests
```sh
pytest

```

### Full Tests
```sh
nox

```
