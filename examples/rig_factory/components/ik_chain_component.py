from rig_factory.abstracts import AbstractRigComponent


class IKChainComponent(AbstractRigComponent):
    Name = 'IKChainComponent'
    Version = 1

    def build(self, **kwargs):
        print('Built {}.'.format(self))


class IKChainComponentNew(IKChainComponent):
    """
    Subclassing abstract subclasses also works (for 
    convenience).
    """
    Version = 2

    def build(self, **kwargs):
        super(IKChainComponentNew, self).build(**kwargs)
        print('Additional changes.')
