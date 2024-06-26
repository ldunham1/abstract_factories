from rig_factory.abstracts import AbstractRigComponent


class IKChainComponent(AbstractRigComponent):
    Name = 'IKChainComponent'
    Version = 1

    def build(self, **kwargs):
        print('Built {}v{}.'.format(self.Name, self.Version))


class IKChainComponentNew(IKChainComponent):
    Version = 2

    def build(self, **kwargs):
        super(IKChainComponentNew, self).build(**kwargs)
        print('Additional changes.')
