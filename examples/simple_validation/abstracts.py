import types


class Context(object):

    def __init__(self, label, data):
        self.label = label
        self.data = data

    def __str__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.label)


class AbstractCollector(object):

    def collect(self):
        # type: () -> types.GeneratorType[Context]
        raise NotImplementedError('collect')


class AbstractValidator(object):

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def validate(self, context):
        # type: (Context) -> list
        raise NotImplementedError('validate')
