"""
Upon importing loads configurations from the files that are provided as
commandline argument with `--config`.
"""
import importlib
import os
import argparse
import warnings
from pathlib import Path
import conf


get = globals().get  # Capture the `get` method from `dict`.


def load(*names, override=True, raise_exception=False):
    """
    Read the given names and load their content into this configuration module.
    :param names: a varg that contains paths (str) to the conf files
    that need to be read or names of environment variables with paths.
    :param override: determines whether previously known configurations need to
    be overridden.
    :param raise_exception: Raise exception on parse failure.
    :return: None.
    """
    for name in names:
        if not name:
            warnings.warn('an empty name is not allowed')
            return
        fname = os.environ.get(name, name)
        file_path = Path(fname)
        suffix = file_path.suffix or 'default'
        if not file_path.exists():
            warnings.warn('conf file "%s" not found' % fname)
            return

        parser_module = _supported_types.get(suffix.lower(), None)
        if not parser_module:
            warnings.warn('cannot parse files of type "%s"' % suffix)
            return

        parse = importlib.import_module(parser_module).parse
        with open(fname) as file:
            try:
                configurations = parse(file)
            except Exception as err:
                warnings.warn('failed to parse "%s". Reason: %s' %
                              (fname, err))
                if raise_exception:
                    raise
                else:
                    return
        for key in configurations:
            if override or not get(key):
                setattr(conf, key, configurations[key])
                globals()[key] = configurations[key]
                _content[key] = configurations[key]


def asdict() -> dict:
    """
    Get the loaded configuration as a dict.
    :return: the config as a dict.
    """
    return _content


_content = {}
_supported_types = {
    '.yml': 'conf.parsers.yaml_parser',
    '.yaml': 'conf.parsers.yaml_parser',
    '.json': 'conf.parsers.json_parser',
    '.ini': 'conf.parsers.ini_parser',
    'default': 'conf.parsers.ini_parser'
}
_help_msg = 'conf file(s) to load. Supported types are: %s' % \
            ', '.join(_supported_types)
_parser = argparse.ArgumentParser()
_parser.add_argument('--config', metavar='conf-file',
                     nargs='+', type=str, help=_help_msg)
_parsed_config = _parser.parse_known_args()[0]

if _parsed_config.config:
    load(*_parsed_config.config, override=True)
