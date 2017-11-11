from json import dumps
from os import environ

from ansig.configurator import ConfigParser


class Generator(object):
    ''' Dynamic inventory generator for Ansible '''

    def __init__(self, filename=None):
        self.config = ConfigParser(filename)
        self.session = self._configure_session()
        self.regions = self._configure_regions()

    @property
    def _default_inventory(self):
        return {'all': {'hosts': [], 'vars': {}}, '_meta': {'hostvars': {}}}

    def _configure_session(self):
        pass

    def _configure_regions(self):
        regions = []

        configured_regions = self.config.get('aws', 'regions').split(',')
        if 'all' in configured_regions:
            excluded_regions = self.config.get('aws', 'regions_exclude')
            for region_info in []:
                if region_info.name not in excluded_regions:
                    regions.append(region_info.name)
        elif 'auto' in configured_regions:
            reg = environ.get('AWS_REGION', environ.get('AWS_DEFAULT_REGION'))
            if reg:
                regions.append(reg)
        else:
            regions = [reg.strip() for reg in configured_regions]

        return regions

    def generate_host_list(self, refresh=False):
        ''' Generates a list of available hosts and their metadata '''

        output = self._default_inventory

        return dumps(output, indent=2)

    def generate_host_info(self, host, refresh=False):
        ''' Generates all the metadata for a specific host '''

        output = {}

        return dumps(output, indent=2)

    def generate_debug_info(self):
        ''' Generates debugging information '''

        output = {
            'regions': self.regions,
            'config': dict((k, v) for (k, v) in self.config.items('aws')),
        }

        return dumps(output, indent=2)
