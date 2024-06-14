import os

from abstract_factories import AbstractTypeFactory

from .abstracts import AbstractRigComponent


class RigComponentBuilder(object):
    """
    This example uses an AbstractTypeFactory as we intend 
    to build multiple rig components from the same 
    type (ie IkChain > IKChain('arm_left'), IKChain('arm_right') etc).

    We're discovering and registering AbstractRigComponent 
    subclasses by path. This reduces the overhead and 
    organisation needed in setting up the component 
    modules and suits a more dynamic environment.
    
    We also assign the AbstractTypeFactory to an
    instance variable rather than subclassing to avoid
    unintentional overrides.
    """

    def __init__(self):
        self.factory = AbstractTypeFactory(
            abstract=AbstractRigComponent,
            paths=[os.path.join(os.path.dirname(__file__), 'components')],
            name_key='Name',  # Removing this will default to class name instead.
            version_key='Version',
        )

    def build(self, component_data):
        """
        Given a list of component data, build the rig.
        :returns list[AbstractRigComponent]: Built component instances.
        """
        results = []
        for data in component_data:
            # Get the component type from the given data.
            # As we're lazily storing build data here 
            # too, we just remove type and version data 
            # as its only used for identity.
            component = self.factory.get(
                data.pop('type'),
                version=data.pop('version', None),
            )

            # We create an instance and as it to build.
            # The instance will likely be needed 
            # later (post build etc).
            instance = component()
            instance.build(**data)
            results.append(instance)

        return results
