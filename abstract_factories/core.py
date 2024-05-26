import inspect
import types

from . import utils
from .constants import LOGGER


# ------------------------------------------------------------------------------
class SimpleFactory(object):

    def __init__(self,
                 abstract,
                 paths=None,
                 modules=None,
                 name_key=None,
                 version_key=None):
        self._abstract = abstract
        self._name_key = name_key or '__name__'
        self._version_key = version_key

        self._items = []

        if paths:
            for path in utils.ensure_iterable(paths):
                self.register_path(path)

        if modules:
            for module in utils.ensure_iterable(modules):
                self.register_module(module)

    # --------------------------------------------------------------------------
    def __repr__(self):
        return '{}(items={})'.format(type(self).__name__, len(self._items))

    # --------------------------------------------------------------------------
    @property
    def abstract(self):
        return self._abstract

    # --------------------------------------------------------------------------
    def _is_viable_item(self, item):
        if not inspect.isclass(item):
            return False
        elif item is self._abstract:
            return False
        elif not issubclass(item, self._abstract):
            return False

        return True

    def _item_is_registered(self, item):
        return item in self._items

    def _prepare_item_for_add(self, item):
        return item

    def _prepare_item_for_remove(self, item):
        return item

    def _add_item(self, item):
        if self._is_viable_item(item):
            prepared_item = self._prepare_item_for_add(item)
            if not self._item_is_registered(prepared_item):
                LOGGER.debug('Adding item {}.'.format(item))
                self._items.append(prepared_item)
                return 1
        return 0

    def _remove_item(self, item):
        prepared_item = self._prepare_item_for_remove(item)
        if self._item_is_registered(prepared_item):
            LOGGER.debug('Removing item {}.'.format(item))
            self._items.remove(prepared_item)
            return 1
        return 0

    # --------------------------------------------------------------------------
    def get_name(self, item):
        """
        Get the name value for <item>.
        :param type item: Abstract subclass to use.
        :rtype: str
        """
        name = getattr(item, self._name_key)
        return name() if callable(name) else name

    def get_version(self, item):
        """
        Get the version value for <item>, if available.
        :param type item: Abstract subclass to use.
        :rtype: int|float|None
        """
        version = None
        if not self._version_key:
            return version

        try:
            version = getattr(item, self._version_key)
        except AttributeError as e:
            LOGGER.debug(
                'Failed to get Version from {} using '
                'version_identifier "{}" :: {}.'.format(item, self._version_key, e)
            )
        return version() if callable(version) else version

    def get(self, name, version=None):
        """
        Get the item matching <name> and <version>.
        If no version is provided, return the first item matching the given name.
        If no matching version is found, return None.
        :param str name: Name to get the item for.
        :param int|float|None version: Version to get. None to get latest.
        :rtype: type|None
        """
        name_matches = (
            item
            for item in self._items
            if self.get_name(item) == name
        )
        versions = {
            self.get_version(item): item
            for item in name_matches
        }
        if not versions:
            LOGGER.warning('{} has no matching items for {}.'.format(self, name))
            return None

        # Return latest version
        if version is None:
            return versions[max(versions)]

        return versions.get(version, None)

    def names(self):
        """
        Get all unique names for registered items.
        :rtype: list[str]
        """
        results = {
            self.get_name(item)
            for item in self._items
        }
        return list(results)

    def versions(self, name):
        """
        Get all versions the registered item using <name> (descending).
        :param str name: Plugin name to get versions for.
        :rtype: list[int|float|None]
        """
        # If we're not able to detect versions, then we don't try to.
        if not self._version_key:
            return []

        results = [
            self.get_version(item)
            for item in self._items
            if self.get_name(item) == name
        ]
        results.sort()
        return results

    def items(self):
        """
        Get the registered items.
        :rtype: list[type]
        """
        results = [
            self.get(name)
            for name in self.names()
        ]
        return results

    def clear(self):
        """Clear the registered items."""
        del self._items[:]

    # --------------------------------------------------------------------------
    def register_item(self, item):
        """
        Register <item> with the factory.
        :param type item: Plugin to register with the factory.
        :return: True if <item> was registered successfully.
        :rtype: bool
        """
        if self._add_item(item):
            return True
        return False

    def deregister_item(self, item):
        """
        Deregister <item> from the factory.
        :param type item: Plugin to deregister with the factory.
        :return: True if <item> was deregistered successfully.
        :rtype: bool
        """
        if self._remove_item(item):
            return True
        return False

    def register_module(self, module):
        """
        Find and register any viable items found in <module>.
        If <module> is a package, sub-modules are not automatically imported or registered.
        ModuleTypes in <module> are not checked, only valid items.
        :param ModuleType module: Path to use.
        :return int: Number of registered items.
        """
        count = 0

        if not isinstance(module, types.ModuleType):
            return count

        for item in module.__dict__.values():
            count += self._add_item(item)

        return count

    def register_path(self, path, recursive=True):
        """
        Find and register any viable items found in <path>.
        :param str path: Path to use.
        :param bool recursive: True to search nested directories. False to only search immediate files.
        :return int: Number of registered items.
        """
        count = 0

        for filepath in utils.iter_python_files(path, recursive=recursive):
            module = utils.import_from_filepath(filepath)
            if module:
                count += self.register_module(module)

        return count
