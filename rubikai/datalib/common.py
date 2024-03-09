INSTRUCTIONS = """

RubikAI error:

    missing `{library}`

This feature requires additional dependencies:

    $ pip install rubikai[datalib]

"""

NUMPY_INSTRUCTIONS = INSTRUCTIONS.format(library="numpy")


class MissingDependencyError(Exception):
    pass
