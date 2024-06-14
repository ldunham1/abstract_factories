from collections import defaultdict

from abstract_factories import AbstractInstanceFactory

from . import abstracts, json_checker


class DataValidator(object):
    """
    Simple Validation example to find and validate data.
    Multiple abstract factories are used (and could be extended on) in
    order to provide the convenience desired;
    - Finding the data to validate.
    - Validating the data.
    - (Optional) Do something else with the validated data.

    AbstractInstanceFactories are used here as we don't need to create
    multiple instances of types. We're only interested in the
    instance (allowing for a singular type to create multiple
    registered instances that have different behaviours - ie collecting
    different file types or from different paths).
    """

    def __init__(self):
        self.collector_factory = AbstractInstanceFactory(
            abstracts.AbstractCollector,
            modules=[json_checker],
        )
        self.validator_factory = AbstractInstanceFactory(
            abstracts.AbstractValidator,
            modules=[json_checker],
        )

    def collect(self):
        """
        Get Contexts found by registered Collectors.
        :rtype: list[Context]
        """
        return [
            context
            for collector in self.collector_factory.items()
            for context in collector.collect()
        ]

    def validate(self, context_list=None):
        """
        Validate Contexts using registered Validators.
        Any validation issues are added to a dictionary identified
        by Context and Validator.
        :rtype: dict[str, dict[str, list[str]]]
        """
        results = defaultdict(dict)

        # Use either given contexts or all available.
        for context in context_list or self.collect():
            for validator in self.validator_factory.items():
                issues = validator.validate(context)
                if issues:
                    results[str(context)][str(validator)] = issues

        # return a native dict type
        return dict(results)
