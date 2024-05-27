# Abstract Factories
`abstract_factories` provides functional factory classes extending the 
loosely based on  Abstract Factory design pattern.
The primary use case is to provide a clear layer of abstraction 
for scalable data.

- Tested on Python 3.8 - 3.12
- Functional on Python 2.7.
  > Wait - what? Python 2.7? What year is this?
  >
  > I have often professionally worked on legacy systems that are too 
  > fragile or large to realistically update to Python 3.
  > Providing there's no functional or notable impact in order to 
  > support 2.7, I have no reason to ignore its existence _yet_.

---

## Overview
On initialisation, the factory is told which abstract type (class) of items it 
should register. It is also told how to determine the name (identifier) and optional 
version. This allows the factory to provide the types or instances it has registered that
best matches these requirements.

---

### Registering
The factory is responsible for storing and accessing either abstract subclasses or their instances 
(see `Item Modes`).

For convenience, the Factories can be told where to find the abstract subclasses or subclass 
instances, which it will attempt to register. 
Otherwise, items can be registered manually, found within a module or recursively from python 
files in directory.

##### Explicit Item Registration
Items can be registered with the factories directly.
`AbstractTypeFactory.register_item(AbstractSubclass)`
`AbstractInstanceFactory.register_item(AbstractSubclass())`


##### Module Item Registration
Items can be discovered in any registered modules. 
This is useful where abstract subclasses are packaged with common functionality (utilities etc).
Only the module's locals are checked, so only items available directly in the registered module are added.

`AbstractTypeFactory.register_module(module)`
`AbstractInstanceFactory.register_module(module)`


##### Path Item Registration
Items can be recursively discovered in any registered paths. 
This is useful where abstract subclasses are independent from each other and is more dynamic in design, for example 
contextually available functionality for extending a tool.
Nested python files are dynamically imported and checked for viable items.

`AbstractTypeFactory.register_path(directory)`
`AbstractInstanceFactory.register_path(directory)`

---

### Item Modes
There are 2 convenient factory classes provided for different use cases of abstract_factories. 
Both have the same interface and functionality, the difference being the format of the 
item being stored. 

##### AbstractTypeFactory
Stores abstract subclasses. 
This is useful when either only classes are needed or multiple 
instances of each type could be needed but stored elsewhere.

##### AbstractInstanceFactory
Stores instances of abstract subclasses. 
This is useful when instances of a type could determine a different version.

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
