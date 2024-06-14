import json
import os

from .abstracts import Context, AbstractCollector, AbstractValidator


class JsonFileCollector(AbstractCollector):
    """
    Simple json file collector.
    """

    def collect(self, path=None, **kwargs):
        for root, _, filenames in os.walk(path or os.getcwd()):
            for filename in filter(lambda x: x.endswith('.json'), filenames):
                filepath = os.path.join(root, filename)
                data = None
                try:
                    with open(filepath, 'r') as fp:
                        data = json.load(fp)
                except Exception:
                    pass
                yield Context(filename, {'type': 'json', 'data': data})


class JsonFileValidator(AbstractValidator):

    def validate(self, context):
        issues = []
        if context.data.get('type') == 'json' and not context.data.get('data'):
            issues.append('No json data deserialized.')
        return issues


# ------------------------------------------------------------------------------
# Create some instances to be discovered and registered.
collector = JsonFileCollector()
validator = JsonFileValidator()
