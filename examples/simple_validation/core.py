from collections import defaultdict

from abstract_factories import AbstractInstanceFactory

from . import abstracts, json_checker


class DataValidator(object):

    def __init__(self):
        self.collector_factory = AbstractInstanceFactory(abstracts.AbstractCollector, modules=[json_checker])
        self.validator_factory = AbstractInstanceFactory(abstracts.AbstractValidator, modules=[json_checker])

    def collect(self):
        return [
            context
            for collector in self.collector_factory.items()
            for context in collector.collect()
        ]

    def validate(self, context_list=None):
        results = defaultdict(dict)
        context_list = context_list or self.collect()
        for context in context_list:
            for validator in self.validator_factory.items():
                issues = validator.validate(context)
                if issues:
                    results[str(context)][str(validator)] = issues
        return results
