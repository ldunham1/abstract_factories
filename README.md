# Abstract Factories 
[![PyPI - Version](https://img.shields.io/pypi/v/abstract-factories)](https://pypi.org/project/abstract-factories/) [![Actions Status](https://github.com/ldunham1/abstract_factories/actions/workflows/python-package.yml/badge.svg)](https://github.com/ldunham1/abstract_factories/actions)  

![Python 2.7 Version](https://img.shields.io/badge/python-2.7-blue)
![Python 3 Versions](https://img.shields.io/pypi/pyversions/pybadges.svg)

A collection of classes to support [Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory) 
design, but with convenience.  
The Abstract Factory design lends itself well to systems that need to scale quickly and safely.  



#### Simple Examples

##### Rigging Framework
See example [rig factory](https://github.com/ldunham1/abstract_factories/tree/main/examples/rig_factory).  
Rig components can often be updated to address bugs, improve performance or introduce features.  
A common unintentional side effect is introducing behavioural regressions or different results.  

This approach encourages the use of versioning to "soft-lock" rig components so when a change is necessary, it 
can be done whilst maintaining the current implementation. The new rig component version is used by default, but 
the previous versions are still immediately accessible for use. 
Better yet, the Abstract Factory design simplifies serialization and deserialization of the data, so older 
rigs can still be built as they were whilst being aware of the potential to upgrade.


##### Asset Validation (Files, Rigs, Models, Animations etc)
See [simple_validation](https://github.com/ldunham1/abstract_factories/tree/main/examples/simple_validation) example.  
Asset validation is relatively simple to implement, but increasingly difficult to manage during a production.  



## Installation
Clone this repo or access it from PyPI;  
`pip install abstract-factories`


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


## Additional

### Contextual `get`:
Instead of a `str` type `name_key` or `version_key` value, you can instead provide a callable. This will be used to 
determine each item's name and/or version.  
This is especially useful when the context of an item's name or version lies outside the Factory's remit.  


## Further Information
Abstract factories is influenced by https://github.com/mikemalinowski/factories.


## License
This project is licensed under the MIT License.
