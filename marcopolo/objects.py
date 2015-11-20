import sys
import json

import yaml


class SerializableObject(object):
    __keys__ = []

    def _serialize(self):
        """Must be defined by subclass"""
        pass

    def to_json(self):
        return json.dumps(self._serialize(), indent=2)

    def to_yaml(self):
        return yaml.dump(self._serialize(), default_flow_style=False,
                explicit_start=True)

    def __str__(self):
        return self.name


class Environment(SerializableObject):
    __keys__ = [ 'aliases',
                 'datacenters',
                 'default',
                 'dependencies',
                 'infrastructure',
                 'tiers' ]

    def __init__(self, **kwargs):
        for key in self.__keys__:
            setattr(self, key, kwargs.get(key, None))

    def _serialize(self):
        out = {self.name: {

            'datacenters': self.datacenters,
            'alias': [str(x) for x in self.aliases],
            'dependencies': self.dependencies,
            'infrastructure': self.infrastructure
            }
        }
        if self.default:
            out[self.name]['default'] = True
        return out

    def set_name(self, name=None, template=None):
        self.name = name
        self.__name_template = template
        if self.name is None:
            self.name = self.__name_template

class Polo(SerializableObject):
    # XXX These are the keys expected in schema_version 0.0.1,
    #         we use this list to confirm data coming in
    __keys__ = [ 'aliases',
                 'desc',
                 'name',
                 'owner',
                 'schema_version',
                 'source',
                 'summary',
                 'tracker',
                 'website' ]

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        for key in self.__keys__:
            setattr(self, key, kwargs.get(key, None))
        self.environments = []
        for e in kwargs.get('environments', {}):
            env = Environment(**e)
            env.set_name(template=kwargs['environment_name_template'])
            self.environments.append(env)

    def _serialize(self):
        out = {}
        for x in self.__keys__:
            out[x] = getattr(self, x)
        out['environments'] = {}
        for x in self.environments:
            out['environments'].update(x._serialize())
        return [out]

def parse(data):
    data = yaml.load(data)
    return Polo(**data[0])

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        for p in parse(f.read()):
            print p.to_yaml()

