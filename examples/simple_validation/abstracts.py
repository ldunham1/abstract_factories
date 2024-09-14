

class Context(object):
    """
    Represents a piece of data to validate.
    Data is found and wrapped as Contexts by Collectors.
    These Contexts are then passed to Validators.
    """

    def __init__(self, label, data):
        self.label = label  # To identify the context.
        self.data = data    # To be used by validators.

    def __repr__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.label)


class AbstractCollector(object):
    """
    A Collector is responsible for finding and wrapping data into individual Contexts.
    Typically, the data is given as a Dictionary as it's mutable and easily queried.
    """

    def collect(self, **kwargs):
        """
        Collect method to be overridden in subclasses to yield collected Context
        objects to be validated.
        :return types.GeneratorType[Context]: Yield collected Contexts.
        """
        raise NotImplementedError('collect')


class AbstractValidator(object):
    """
    A Validator will validate the data in a Context.
    It can return a list of any issues found.
    As Context data is mutable, if an autofix can be applied, the data can be
    modified before continuing to the next Validator.
    """

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def validate(self, context):
        """
        Validate method to be overridden by subclasses.
        Issues found by this validator should be put into a list and returned.
        :param Context context: Context to validate.
        :return list[str]: List of issues found during validation.
            An empty list is considered a success.
        """
        raise NotImplementedError('validate')
