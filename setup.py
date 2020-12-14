import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="borsh",
    version="0.0.1",
    author="Bohdan Khorolets",
    author_email="bogdan@khorolets.com",
    description="Borsh is an implementation of the Borsh binary serialization format for Python projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khorolets/borsh-py",
    packages=setuptools.find_packages(),
    license="(MIT OR Apache-2.0)",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.5',
)
