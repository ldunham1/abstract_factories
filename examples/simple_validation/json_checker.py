import json
import os

from .abstracts import Context, AbstractCollector, AbstractValidator


class JsonFileCollector(AbstractCollector):

    def collect(self):
        for root, _, filenames in os.walk(os.getcwd()):
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
collector = JsonFileCollector()
validator = JsonFileValidator()
