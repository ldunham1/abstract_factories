from rig_factory.abstracts import AbstractRigComponent


class AbstractIKComponent(AbstractRigComponent):
    Name = 'AbstractIKComponent'
    Version = 1

    # Dont register this class
    Registerable = False

    def build(self, **kwargs):
        print('Built {}.'.format(self))


class IKChainComponent(AbstractIKComponent):
    Name = 'IKChainComponent'
    Version = 1

    # Register this class and its subclasses
    Registerable = True

    def build(self, **kwargs):
        super(IKChainComponent, self).build(**kwargs)


class IKChainComponentJacobian(IKChainComponent):
    Version = 2

    def build(self, **kwargs):
        super(IKChainComponentJacobian, self).build(**kwargs)
