# Abstract Factories 
[![PyPI - Version](https://img.shields.io/pypi/v/abstract-factories)](https://pypi.org/project/abstract-factories/) [![Actions Status](https://github.com/ldunham1/abstract_factories/actions/workflows/python-package.yml/badge.svg)](https://github.com/ldunham1/abstract_factories/actions)

A collection of classes to support the Abstract Factory design pattern, providing a clear abstraction 
layer for scalable data in dynamic environments.  

`abstract_factories` will auto-register viable items from any given python **module** and/or **path**.  


- Tested on Python 3.7 - 3.12
- Functional on Python 2.7
  > Wait - what? Python 2.7? What year is this?  
  > I often work professionally on legacy systems that are too 
  > fragile or large to update.
  > Providing there's no functional or notable impact 
  > supporting 2.7, I have no reason to ignore its existence _yet_.

---

## Installation
```bash
pip install abstract-factories
```

---

## Usage
Initialize AbstractTypeFactory or AbstractInstanceFactory with an abstract type.  
Optionally, provide the attribute/method name to identify items by name (and optionally version).

Registering items can be done directly.
```python
from abstract_factories import AbstractTypeFactory


class AbstractVehicle(object):
    def start(self):
        raise NotImplementedError()


class Car(AbstractVehicle):
    def start(self):
        print('Vrooom...')


# Type Factory
type_factory = AbstractTypeFactory(AbstractVehicle)
type_factory.register_item(Car)
assert type_factory.get('Car') is Car
```

By default, items are referred to by class name, unless a name_key is provided.


Abstract factories can automatically register items found in given python modules or paths.
```python
from abstract_factories import AbstractTypeFactory
from . import my_vehicle_package


# Type Factory
type_factory = AbstractTypeFactory(my_vehicle_package.AbstractVehicle)

# Find any AbstractVehicle subclasses in `my_vehicle_package` and register them.
type_factory.register_module(my_vehicle_package)
assert type_factory.get('Car') is my_vehicle_package.Car

# Can also find any AbstractVehicle subclasses in a directory and register those too.
type_factory.register_path('c:/Users/user/downloads/other_vehicles')
```


In some use-cases, instances are a much better fit for the type of data you want to use in your factory (a factory of factories?).  
In that case, use `AbstractInstanceFactory`.
```python
from abstract_factories import AbstractInstanceFactory


class AbstractVehicle(object):
    def __init__(self, make=None):
        self.make = make

    def start(self):
        raise NotImplementedError()


class Car(AbstractVehicle):
    def start(self):
        print('Vrooom...')


# Instance Factory
honda = Car('Honda')
instance_factory = AbstractInstanceFactory(AbstractVehicle, name_key='make')
instance_factory.register_item(honda)
assert instance_factory.get('Honda') is honda
```

### Registration:
Register viable items directly.
- `type_factory.register_item(AbstractSubclass)`
- `instance_factory.register_item(AbstractSubclass())`

Find and register any viable items found in the module's locals.
- `type_factory/instance_factory.register_module(module)`  

Find and register any viable items found in any nested python file from a dynamic 
import. Some limitation using relative imports.  
- `type_factory/instance_factory.register_path(r'c:/tools/tool_plugins')`
- `type_factory/instance_factory.register_path(r'c:/tools/tool_plugins/plugin.py')`

---

## Practical Applications
Some examples of practical applications for `abstract_factories` in a production environment.

### Data Validation and Contextual Modification
Use multiple factories together to design scalable Validation, Publishing, Batching, Playlist 
etc frameworks.  
The simplicity of this design allows for quick iteration during development, conditional 
validation, scalability and more.  
See the [simple_validation](examples/simple_validation) example.


### Content Creation - Rigging
Useful for managing production needs in Film, TV, and Games, allowing easy modifications and versioning of components.  
Easily support and modify rig component behaviours during production.  
See the [rig_factory](examples/rig_factory) example.

## Advanced: 
These topics are for more advanced usage of `abstract_factories`.

### Contextual `get`:
Instead of a `str` type `name_key` or `version_key` value, you can instead provide a callable. This will be used to 
determine each item's name and/or version.  
This is especially useful when the context of an item's name or version lies outside the Factory's remit.  
> ! Warning: A conditional `name_key` or `version_key` may result in unexpected behaviour if not managed correctly.

---

## Testing
`.tests/` directory contains examples for;
- Adding, removing & comparing items directly.
- Adding, removing & comparing items found in modules and/or paths.

---

## Further Information
Abstract factories is influenced by https://github.com/mikemalinowski/factories.

---

## License
This project is licensed under the MIT License.
