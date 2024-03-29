from nox_poetry import session  # type: ignore


@session(python=["3.9", "3.8.3"])
def tests(session):  # noqa: D103,WPS442
    session.run_always("poetry", "install", external=True)
    session.install(".")
    session.run("pytest", external=True)
