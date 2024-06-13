from rig_factory.abstracts import AbstractRigComponent


class FKChainComponent(AbstractRigComponent):
    Name = 'FKChainComponent'
    Version = 1

    def build(self, **kwargs):
        print('Built {}.'.format(self))


class FKChainComponentNew(FKChainComponent):
    Version = 2

    def build(self, **kwargs):
        super(FKChainComponentNew, self).build(**kwargs)
        print('Additional changes.')
