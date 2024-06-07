# Abstract Factories 
[![PyPI - Version](https://img.shields.io/pypi/v/abstract-factories)](https://pypi.org/project/abstract-factories/) [![Actions Status](https://github.com/ldunham1/abstract_factories/actions/workflows/python-package.yml/badge.svg)](https://github.com/ldunham1/abstract_factories/actions)  

![Python 2.7 Version](https://img.shields.io/badge/python-2.7-blue)
![Python 3 Versions](https://img.shields.io/pypi/pyversions/pybadges.svg)

[Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory) lends itself well to systems that 
need to scale quickly and safely, allowing users to build and interact with code constructs through names.  
Typically, additional functionality is required to ensure this design fits into a framework well, and even more work 
to allow for speedy iteration and development.  

`abstract_factories` is a collection of classes to support this design with those additional conveniences built-in.
- automatic (dynamic) registration from paths or modules
- simple or conditional querying
- versioning  
- type or instance items

and more. 


## Example Usage

### Tool Versioning
Imagine you have a simple action you want to apply, already using the Abstract Factory design.
```python
from .abstracts import ActionAbstract

class DemoAction(ActionAbstract):
    Version = 1

    def apply(self):
        print('Applied Demo.')
```

You then need to create a new action that addresses a bug BUT its old behavior is still required in places.  
You can use `abstract_factories` to provide the correct version contextually.
```python
from .abstracts import ActionAbstract

class MyAction(ActionAbstract):
    Version = 2

    def apply(self):
        logging.info('Applied Demo.')
```

Now we just create a tool factory and tell it where to find these tools.
```python
import abstract_factories
from .abstracts import ActionAbstract
from . import actions

tool_factory = abstract_factories.AbstractTypeFactory(ActionAbstract, version_key='Version')
tool_factory.register_module(actions)

demo_action = tool_factory.get('DemoAction')  # Automatically retrieves latest.
old_demo_action = tool_factory.get('DemoAction', version=1)
```


### Rigging Frameworks
See [rig factory](https://github.com/ldunham1/abstract_factories/tree/main/examples/rig_factory).  
Rig components can often be updated to address bugs, improve performance or introduce features.  
A common unintentional side effect is introducing behavioural regressions or different results.  

`abstract_factories` encourages the use of versioning to "soft-lock" components so when a change is necessary, it 
can be done safely. The new rig component version is used by default, but the previous versions are still accessible at 
the same time. 
Better yet, the Abstract Factory design simplifies serialization and deserialization of the data, so older 
rigs can still be built as they were whilst being aware of the potential to upgrade.


### Validation Frameworks (Files, Rigs, Models, Animations etc)
See [simple_validation](https://github.com/ldunham1/abstract_factories/tree/main/examples/simple_validation).  
Asset validation is relatively simple to implement, but increasingly difficult to manage during a production.  
Some validation frameworks, like [Pyblish](https://pyblish.com/) manages this well.  

`abstract_factories` provides the minimum required to build your own similar Validation framework. Its 
item auto-registration provides a very flexible environment to quickly develop, improve, iterate and scale 
as you see fit.


## Installation
Clone this repo or access it from PyPI;  
```bash
pip install abstract-factories
```


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

##### Items:
Register viable items directly.
> See `./tests/test_abstract_factories_items.py` for examples.
- `type_factory.register_item(AbstractSubclass)`
- `instance_factory.register_item(AbstractSubclass())`


##### Modules:
Find and register any viable items found directly in the module's locals.  
Optionally, you can enable recursive searching with the `recursive` argument. 
Any additionally imported module in the registered module will be registered also.
> See `./tests/test_abstract_factories_modules` for examples.
- `type_factory/instance_factory.register_module(module)`  
- `type_factory/instance_factory.register_module(module, recursive=True)`  


##### Paths:
Find and register any viable items found in any nested python file from a dynamic import.  
Python files with relative imports loaded this way will fail due to dynamic importing. 
If you want/need to use relative imports, it's recommended to use `register_module` 
method instead for the time being.  
Optionally, you can disable recursive searching with the `recursive` argument.
> See `./tests/test_abstract_factories_paths` for examples.
- `type_factory/instance_factory.register_path(r'c:/tools/tool_plugins/plugin.py')`
- `type_factory/instance_factory.register_path(r'c:/tools/tool_plugins')`
- `type_factory/instance_factory.register_path(r'c:/tools/tool_plugins', recursive=False)`  


## Additional

### Contextual `get`:
Instead of a `str` type `name_key` or `version_key` value, you can instead provide a callable. This will be used to 
determine each item's name and/or version.  
This is especially useful when the context of an item's name or version lies outside the Factory's remit.  


## Further Information
Abstract factories is influenced by https://github.com/mikemalinowski/factories.


## License
This project is licensed under the MIT License.
