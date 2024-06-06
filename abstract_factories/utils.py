import inspect
import os
import pkgutil
import re
import sys
import types
import uuid

from .constants import LOGGER


try:
    basestring
except NameError:
    basestring = str


PYTHON_FILENAME_PATTERN = re.compile(
    r'[^_ \d]?[\w]*?'   # Doesn't start with number, space or underscore
    r'\.py[c]?$'        # Ends with .py, .pyc
)


# ------------------------------------------------------------------------------
# Generate a python version compatible import from file function
if sys.version_info >= (3, 5):
    import importlib.util

    def _import_from_filepath(module_name, filepath):
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

elif sys.version_info >= (3, 0):
    from importlib.machinery import SourceFileLoader
    import importlib.util

    def _import_from_filepath(module_name, filepath):
        ext = os.path.splitext(filepath)[1]
        if ext == '.py':
            module = SourceFileLoader(module_name, filepath).load_module()
        elif ext == '.pyc':
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        else:
            raise ImportError('File type "{}" not supported (.py or .pyc only).'.format(ext))
        return module

# -- Python 2.7
else:
    # noinspection PyUnresolvedReferences
    import imp

    def _import_from_filepath(module_name, filepath):
        ext = os.path.splitext(filepath)[-1]
        if ext == '.py':
            module = imp.load_source(module_name, filepath)
        elif ext == '.pyc':
            with open(filepath, 'rb') as fp:
                module = imp.load_compiled(module_name, filepath, fp)
        else:
            raise ImportError('File type "{}" not supported (.py or .pyc only).'.format(ext))
        return module


if sys.version_info >= (3, 10):
    STANDARDLIB_MODULE_NAMES = frozenset(sys.stdlib_module_names)
else:
    from stdlib_list import stdlib_list
    STANDARDLIB_MODULE_NAMES = frozenset(stdlib_list('{}.{}'.format(*sys.version_info)))


def _import_from_package(module_name, filepath, package):
    if os.path.isfile(filepath):
        filepath = os.path.splitext(filepath)[0]

    root_path, name = os.path.split(filepath)
    for _ in range(package.count('.') + 1):
        root_path = os.path.dirname(root_path)

    module_path = package + '.' + name

    # We ensure the package itself is discoverable for import.
    sys.path.append(root_path)
    module_already_available = module_path in sys.modules
    try:
        # TODO: Currently only modifies module name on surface level (unlike `imp.load_source'/SourceFileLoader etc).
        #  This creates some disparity between loading as a file or via a package.
        #  One option could be to duplicate the given file as the desired name and import that to ensure the module
        #  name matches but this again could lead to unexpected issues when being used elsewhere.

        # Import the fully resolved module name then reassign it to our given name.
        importlib.import_module(module_path)
        module = sys.modules[module_path]

        # Remove the module if it wasn't already available
        if not module_already_available:
            sys.modules.pop(module_path)

        module.__name__ = module_name
    finally:
        sys.path.pop()
    return module


# ------------------------------------------------------------------------------
def is_module(obj):
    """
    Get if <obj> is a module.
    :param object obj: Object to check.
    :rtype: bool
    """
    return isinstance(obj, types.ModuleType)


def ensure_iterable(objects):
    """
    Convenience function to ensure <objects> is iterable, returning a list if not.
    If objects is string type, [objects] is returned.
    :param any objects: Objects to affect.
    :rtype: list, tuple, set, frozenset, types.GeneratorType
    """
    if not objects:
        return []

    if isinstance(objects, (list, tuple, set, frozenset, types.GeneratorType)):
        return objects
    elif isinstance(objects, basestring):
        return [objects]

    return list(objects)


def generate_unique_name_from_filepath(filepath):
    """
    Generate a unique name from <filepath>.
    :param str filepath: Filepath to use.
    :rtype: str
    """
    filename = os.path.splitext(os.path.basename(filepath))[0]
    return '{}_{}'.format(filename, uuid.uuid4().hex)


def find_import_path(path):
    """
    Find the longest, viable import path from <path>.

    .. code-block:: python

        >>> find_import_path('D:/Projects/abstract_factories/tests/test_abstract_factories_paths/packaged_directory')
        'tests.test_abstract_factories_paths.packaged_directory'
        >>> find_import_path('D:/Projects/abstract_factories/tests/test_abstract_factories_paths/packaged_directory/vehicles.py')
        'tests.test_abstract_factories_paths.packaged_directory.vehicles'

    :param str path: Directory or filepath to use.
    :rtype: str
    """
    parts = []

    def build_import_path(directory_, name_, check_module):
        for importer, modname, is_package in pkgutil.walk_packages([directory_]):
            if modname == name_ and check_module != is_package:
                parts.append(modname)
                build_import_path(*os.path.split(directory_), check_module=False)

    is_module = os.path.isfile(path)
    directory, name = os.path.split(path)
    if is_module:
        name = os.path.splitext(name)[0]
    build_import_path(directory, name, check_module=is_module)
    return '.'.join(reversed(parts[1:])) if parts else ''


def import_from_path(filepath, module_name=None):
    """
    Import <filepath> as a ModuleType called <module_name> (auto-generated if None given).
    :param str filepath: Filepath to import as module.
    :param Optional[str] module_name: Module name to import as.
    :rtype: ModuleType
    """
    module_name = module_name or generate_unique_name_from_filepath(filepath)
    module = None
    package = find_import_path(filepath)
    try:
        LOGGER.debug('Loading "{}" into modulename "{}".'.format(filepath, module_name))
        if package:
            module = _import_from_package(module_name, filepath, package)
        else:
            module = _import_from_filepath(module_name, filepath)
        if not module:
            raise TypeError('Only .py and .pyc files are supported. Received "{}".'.format(filepath))
    except Exception as e:
        LOGGER.exception('Failed to load from "{}" :: {}.'.format(filepath, e))
    return module


def get_source_filepath(obj):
    """
    Get the source filepath of <obj>.
    :param object|type|ModuleType obj: Object to check.
    :rtype: str
    """
    if not inspect.ismodule(obj):
        return inspect.getfile(obj)
    elif not inspect.isclass(obj):
        obj = obj.__class__

    try:
        source_filepath = inspect.getsourcefile(obj)
    except TypeError:
        source_filepath = ''
    return source_filepath


def normalise_path(path):
    """
    Expand and normalise <path> to its real path.
    os.sep is replaced with os.altsep (where applicable).
    :param str path: Path to normalise.
    :rtype: str
    """
    norm_path = os.path.normcase(os.path.normpath(os.path.realpath(path)))
    if os.altsep:
        norm_path = norm_path.replace(os.sep, os.altsep)
    return norm_path


def iter_python_files(path, recursive=True):
    """
    Iterate the python files found from <path>.
    If <path> is a python file, yield that.
    If <path> is a directory, iterate nested python files.
    :param str path: Path to find python files from.
    :param bool recursive: True to iterate recursively.
    :rtype: Generator[str]
    """
    # TODO: Handle .zip python packages.
    if os.path.isfile(path):
        if PYTHON_FILENAME_PATTERN.match(os.path.basename(path)):
            yield normalise_path(path)
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for filename in files:
                if not PYTHON_FILENAME_PATTERN.match(filename):
                    continue

                yield normalise_path(os.path.join(root, filename))

            if not recursive:
                break
    else:
        LOGGER.error('iter_python_files >> {} is not an existing file or directory.'.format(path))
        return


def module_is_standardlib(module):
    """
    Get if the module is part of the standard python library.
    :param ModuleType module: Module to test.
    :rtype: bool
    """
    module_name = module.__name__.split('.', 1)[0]
    return module_name in STANDARDLIB_MODULE_NAMES


def iter_python_modules(module, recursive=False, _seen=None):
    """
    Iterate the python modules found in <module>.
    If <module> is a directory, iterate nested python files.
    :param ModuleType module: Root module to find nested modules in.
    :param bool recursive: True to iterate recursively.
    :rtype: Generator[ModuleType]
    """
    if not isinstance(module, types.ModuleType):
        LOGGER.error('iter_python_modules >> {} is not a ModuleType.'.format(module))
        return

    _seen = _seen or set()
    if module in _seen:
        return

    _seen.add(module)
    for value in module.__dict__.values():
        if isinstance(value, types.ModuleType):
            yield value
            if recursive and value not in _seen:
                for submodule in iter_python_modules(value, recursive, _seen=_seen):
                    yield submodule
