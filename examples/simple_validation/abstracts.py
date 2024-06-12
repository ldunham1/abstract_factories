import types


class Context(object):
    """
    Represents a piece of data to validate.
    Data is found and wrapped as Contexts by Collectors.
    These Contexts are then passed to Validators.
    """

    def __init__(self, label, data):
        self.label = label
        self.data = data

    def __str__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.label)


class AbstractCollector(object):
    """
    A Collector is responsible for finding and wrapping data into individual Contexts.
    Typically, the data is given as a Dictionary as it's mutable and easily queried.
    """

    def collect(self):
        # type: () -> types.GeneratorType[Context]
        raise NotImplementedError('collect')


class AbstractValidator(object):
    """
    A Validator will validate the data in a Context.
    It can return a list of any issues found.
    As Context data is mutable, if an autofix can be applied, the data can be modified before continuing to the next Validator.
    """

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def validate(self, context):
        # type: (Context) -> list
        raise NotImplementedError('validate')
