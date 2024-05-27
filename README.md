# Abstract Factories
Clean classes to support [Abstract Factory design pattern](https://refactoring.guru/design-patterns/abstract-factory/python/example#example-0) with 
some additional convenience.  
The primary use case is to provide a clear layer of abstraction for scalable data 
in a dynamic environment.

- Tested on Python 3.8 - 3.12
- Functional on Python 2.7
  > Wait - what? Python 2.7? What year is this?  
  > I often work professionally on legacy systems that are too 
  > fragile or large to update.
  > Providing there's no functional or notable impact 
  > supporting 2.7, I have no reason to ignore its existence _yet_.

---

## Usage:
Initialise `AbstractTypeFactory`/`AbstractInstanceFactory` with the abstract type to respect.  
Optionally provide the attribute/method name to identify items by name (and optionally version).
> If a name identifier is not provided, the subclass name `__name__` is used by default.

This allows the factory to determine the registered items that
best matches base requirements (name and optionally, version).  
```python
from abstract_factories import AbstractTypeFactory, AbstractInstanceFactory

class AbstractVehicle(object):
    def __init__(self, make=None):
        self.make = make

    def start(self):
        raise NotImplementedError()

class Car(AbstractVehicle):
    def start(self):
        print('Vrooom...')

# Type Factory
type_factory = AbstractTypeFactory(AbstractVehicle)
type_factory.register_item(Car)
assert type_factory.get('Car') is Car

# Instance Factory
honda = Car('Honda')
ford = Car('Ford')
instance_factory = AbstractInstanceFactory(AbstractVehicle, name_key='make')
instance_factory.register_item(honda)
instance_factory.register_item(ford)
assert instance_factory.get('Honda') is honda
assert instance_factory.get('Ford') is ford
```

---

### Registration:
The factory is responsible for storing and accessing either abstract subclasses or their instances 
(see `Item Modes`).

For convenience, the Factories can be told where to find the abstract subclasses or subclass 
instances, which it will attempt to register.  
Otherwise, items can be registered manually, found within a module or recursively from python 
files in directory.

Items can be registered with the factories directly.
- `register_item(AbstractSubclass)`
- `register_item(AbstractSubclass())`

Items can be discovered in any registered modules.  
- `register_module(module)`  
  Will find and register any viable items found in the module's locals.

Items can be recursively discovered in any registered paths.  
- `register_path(r'c:/work/tools/my_tool_plugins')`
- `register_path(r'c:/work/tools/my_tool_plugins/specific_plugin.py')`
  Will find and register any viable items found in any nested python file from 
  a dynamic import. This currently has some limitations in terms of relative imports 
  in these files.

---

## Practical Applications
#### Content Creation
`abstract_factories` can be used to keep on-top of scaling production needs (Film, TV, Games).

###### Rigging
For rig building its typical during production to modify rig component behaviours during production (bugfixes, 
performance improvements or additional features). The typical issue is supporting rig component versions for legacy reasons.
Here, its relatively trivial to author a new IKChainComponent (subclassed from the old), modify the behaviour and be 
identified as another version.
```python
class AbstractRigComponent(object):
    Name = 'AbstractRigComponent'
    Version = 0

    def build(self, **kwargs):
        raise NotImplemented

    
class IKChainComponent(AbstractRigComponent):
    """Inverse Kinematics (IK) chain rig component."""
    Name = 'IKChainComponent'
    Version = 1

    def build(self, **kwargs):
        pass

    
class IKChainComponentNew(IKChainComponent):
    """Newer version of Inverse Kinematics (IK) chain rig component."""
    Version = 2

    def build(self, **kwargs):
        super(IKChainComponentNew, self).build(**kwargs)
        print('Made better.')


class FKChainComponent(AbstractRigComponent):
    """Forward Kinematics (FK) chain rig component."""
    Name = 'FKChainComponent'
    Version = 1

    def build(self, **kwargs):
        pass


# --------------------------------------------------------------------------
from abstract_factories import AbstractTypeFactory
from . import components

class RigComponentBuilder(object):
    def __init__(self):
        self.rig_component_factory = AbstractTypeFactory(
            abstract=components.AbstractRigComponent,
            modules=[components],
            name_key='Name', 
            version_key='Version',
        )
    
    def build(self, component_data):
        results = []
        # Get component classes and create instances.
        for data in component_data:
            component = self.rig_component_factory.get(data.pop('type'), version=data.pop('version', None))
            instance = component()
            instance.build(**data)
            results.append(instance)
        return results

# Create an instance of the builder and build a rig from some data.
builder = RigComponentBuilder()
builder.build(
    [
        {'type': 'FKChainComponent', 'name': 'spine'},
        {'type': 'IKChainComponent', 'name': 'arm', 'side': 'left'},
        {'type': 'IKChainComponent', 'name': 'arm', 'side': 'right'},
        {'type': 'IKChainComponent', 'name': 'leg', 'side': 'left', 'version': 2},
        {'type': 'IKChainComponent', 'name': 'leg', 'side': 'right', 'version': 2},
    ]
)
```

---

## Testing
`.tests` directory contains examples for;
- Adding, removing & comparing types and instances of items directly.
- Adding, removing & comparing types and instances of items found in a module.
- Adding, removing & comparing types and instances of items found recursively in a path.

---

## Further Information
Abstract factories is influenced by https://github.com/mikemalinowski/factories.
