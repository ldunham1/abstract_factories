# Abstract Factories
`abstract_factories` provides functional factory classes extending the 
loosely based on  Abstract Factory design pattern.
The primary use case is to provide a clear layer of abstraction 
for scalable data.

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


### Examples
`.tests` directory contains examples for;

- Adding, removing & comparing types and instances of items directly.
- Adding, removing & comparing types and instances of items found in a module.
- Adding, removing & comparing types and instances of items found recursively in a path.


### Influences
Abstract factories is influenced by https://github.com/mikemalinowski/factories.
