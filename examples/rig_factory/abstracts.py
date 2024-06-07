class AbstractRigComponent(object):
    Name = 'AbstractRigComponent'
    Version = 0

    def __str__(self):
        return '{}(v={})'.format(self.Name, self.Version)

    def build(self, **kwargs):
        raise NotImplementedError('build')
