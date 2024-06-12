"""
This example uses `abstract_factories` to find, register and manage 
AbstractRigComponent subclasses.

A typical issue with rig component management is reliability managing 
rig component versions, as latest versions should be used by default but 
earlier versions should still be accessible when needed.

This is made easy with the Type Factory.
Intentionally grouping AbstractRigComponent subclasses by class name 
promotes the good practice of ensuring component versions are not from the 
same module (reduces risk of accidental modification and easier to debug) and 
then sorts by their Version identifier.
The `factory.get()` method will return the latest versioned item, unless a 
version value is given.

Unlike traditional Factory and Abstract Factory designs, interactions with 
the items directly is encouraged, but ensure the abstract itself provides all 
expected abstract methods and parameters.
"""
from .core import RigComponentBuilder
