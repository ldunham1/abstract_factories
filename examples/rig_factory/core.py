import os

from abstract_factories import AbstractTypeFactory

from .abstracts import AbstractRigComponent


class RigComponentBuilder(object):

    def __init__(self):
        self.factory = AbstractTypeFactory(
            abstract=AbstractRigComponent,
            paths=[os.path.join(os.path.dirname(__file__), 'components')],
            name_key='Name',
            version_key='Version'
        )

    def build(self, component_data):
        results = []
        for data in component_data:
            component = self.factory.get(
                data.pop('type'),
                version=data.pop('version', None),
            )
            instance = component()
            instance.build(**data)
            results.append(instance)
        return results
