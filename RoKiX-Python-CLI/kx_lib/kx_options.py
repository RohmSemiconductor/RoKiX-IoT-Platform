# 
# Copyright 2018 Kionix Inc.
#
# pylint: disable=W0622
from configparser import ConfigParser, NoSectionError
from argparse import ArgumentParser, ArgumentError

from jsonschema import Draft6Validator
from jsonschema.exceptions import ValidationError

from kx_lib.kx_cfg_schema import CfgSchema


def str_to_bool(value):
    if value.lower() in ['true', '1','on'] :
        return True
    elif value.lower() in ['false','0','off']:
        return False
    else:
        raise ValueError


def null(value):
    if isinstance(value, str) and len(value) == 0:
        return None
    #Python2
    if isinstance(value,unicode) and len(value)==0:
        return None
    return value

def _str(string):
    if len(string) == 0:
        return None
    return str(string)

VALUE_MAPPINGS = {
    "integer": int,
    "string": _str,
    "boolean": str_to_bool,
    "number": float,
    "null": null
}

TYPE_MAPPING = {
    "integer": int,
    "string": str,
    "boolean": bool,
    "number": float,
    "null": type(None)
}


class EvkitConfigurations(ArgumentParser):
    ROKIX_FILE_LOCATIONS = [
        '../../rokix_settings.cfg',
        '../rokix_settings.cfg',
        'rokix_settings.cfg'
    ]

    BASE_SECTIONS = ['board', 'bus2', 'generic']

    def __init__(
            self,
            filenames=None,
            schema=CfgSchema(),
            include_sections=None
    ):
        super(EvkitConfigurations, self).__init__(description='Example: %(prog)s -s')
        if filenames is None:
            filenames = self.ROKIX_FILE_LOCATIONS
        if include_sections is None:
            include_sections = self.BASE_SECTIONS
        else:
            include_sections.extend(self.BASE_SECTIONS)
        self.schema = schema
        self.arg_validator = Draft6Validator(schema)
        self._schema_properties = self.schema['properties']

        self.evkit_config = ConfigParser(
            inline_comment_prefixes=(';', '#'),
            allow_no_value=True,
            delimiters=('='),
            dict_type=dict
        )
        self.config_file = self.evkit_config.read(filenames)

        self._config_options = []
        self._sections = self.evkit_config.sections()
        
        assert self.evkit_config.getint('root', 'version') == 2, 'Invalid cfg file version on file %s' % self.config_file

        # Add base sections to cmd args
        for section in self._sections:
            if section in include_sections:
                self.add_section_args(section)


    def add_section_args(self, section):
        if section not in self._sections:
            raise ValueError("Invalid section")
        for option, value in self.evkit_config.items(section):
            self._add_config_arg(option, value)

    def _check_option(self, option, value):
        '''
            Maps option to its type as specified in schema, if exists
        '''
        if self._schema_properties.get(option, None) is None:
            return type(value), value
        # property can have multiple types
        if isinstance(self._schema_properties[option]['type'], list):
            initial_value = value
            for _type in self._schema_properties[option]['type']:
                map = VALUE_MAPPINGS[_type]
                try:
                    value = map(value)
                # if the config value cannot be mapped to type defined by schema
                except ValueError:
                    value = initial_value
                else:
                    if self.arg_validator.is_valid({option:value}):
                        if _type =='null':
                            # Null type value does not have proper mapping type
                            _type = [
                                val for val in self._schema_properties[option]['type']][0] 
                        return TYPE_MAPPING[_type], value
            raise ValueError('Option %s has invalid value %s' %(option, initial_value))
        else:
            _type = self._schema_properties[option]['type']
            map = VALUE_MAPPINGS[self._schema_properties[option]['type']]
            try:
                value = map(value)
            except ValueError:
                value = value
            if self.arg_validator.is_valid({option:value}):
                return TYPE_MAPPING[_type], value
            # Value is not of specified type
            raise ValueError('Option %s has invalid value %s' % (option, value))
                    


    def _add_config_arg(self, option, default):
        setattr(self, option, default)
        option_dtype, default = self._check_option(option, default)             
        short_hand = self.schema['properties'].get(option, {}).get('title', None)
        _help = 'Override {} (Current value: "{}") setting from .cfg'.format(
            option, default
        )
        help = self.schema['properties'].get(option, {}).get('description', _help)
        examples = self.schema['properties'].get(
            option, {}).get('examples', None)
        if examples is not None:
            help += '; Examples:{}'.format(', '.join(examples))
        help += '; Default:"{}"'.format(default)
        choices = self.schema['properties'].get(option, {}).get('enum', None)
        if isinstance(default, bool):
            option_dtype = str_to_bool

        if short_hand is None:
            self.add_argument(
                '--' + option,
                default=default, type=option_dtype,
                choices=choices,
                help=help
            )
        else:
            self.add_argument(
                short_hand,
                '--' + option,
                default=default, type=option_dtype,
                choices=choices,
                help=help
            )


    def add_argument(self, *args, **kwargs):
        '''
            Overrides parent method
        '''
        try:
            super(EvkitConfigurations, self).add_argument(*args, **kwargs)
        except ArgumentError:
            return
        for arg in args:
            if arg.count('-') == 2:
                option = arg.lstrip('--')
            elif arg.count('-') == 0:
                option = arg

        if option != 'help' and option not in self._config_options:
            self._config_options.append(option)
            setattr(self, option, kwargs.get('default', None))

    def has_option(self, option):
        condition = hasattr(self, option)
        if not condition:
            return False
        return True

    def __delattr__(self, option):
        self._config_options.remove(option)
        super(EvkitConfigurations, self).__delattr__(option)

    def set(self, key, value):
        setattr(self, key, value)

    def get(self, option, default=None):
        try:
            val = getattr(self, option)
        except AttributeError:
            return default
        else:
            return val

    def parse_args(self, args=None, namespace=None):
        '''
            Overrides parent method
        '''
        if namespace is None:
            namespace = self
        return super(EvkitConfigurations, self).parse_args(args=args, namespace=namespace)

    def keys(self):
        return self._config_options

    def __getitem__(self, key):
        return getattr(self, key)

    def as_dict(self):
        return {key: getattr(self, key) for key in self._config_options}
