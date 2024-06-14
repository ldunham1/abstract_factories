"""
This example uses `abstract_factories` to create multiple instance factories
find, register and manage subclass instances of different abstracts for
specific roles.
This design is inspired by [Pyblish](https://pyblish.com/).

A typical issue with validation management is increasing complexity and
scaling with production to remain effective.

This is made relatively simple using multiple Factories.
Collector and Validator instances are found from a [given module](./json_checker.py).
The objects to be validated `Contexts` are collected by the registered Collectors and
validated by each registered Validator.

Collection can be hardcoded or given arguments (as shown in the example), provided other
viable Collectors handle additional, unwanted kwargs.
Validators return a list of issues (if any) and the `DataValidator` class manages
any logic needed to report this to the user.

The simplicity of the design ensures that as more validation checks are needed, it is
possible to add need validators to the discovery paths or be injected via modules or
even directly. Because the factories are instance based, the same type could be reused
with different arguments and utilised as separate collectors.
One additional feature to improve scalability would be the concept of `Families/Groups`.
This would allow Contexts to be filtered to match with only relevant Validators, allowing
a single DataValidator class to manage multiple types of validation at the same time.
"""
from .core import DataValidator
