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
        return self.alias


class Environment(SerializableObject):
    __keys__ = ['tier', 'datacenters', 'aliases', 'dependencies',
            'infrastructure', 'default']

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


class Polo(SerializableObject):
    # XXX These are the keys expected in schema_version 0.0.1,
    #         we use this list to confirm data coming in
    __keys__ = ['schema_version', 'name', 'alias', 'summary', 'desc',
            'source', 'tracker', 'website', 'owner']

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        for key in self.__keys__:
            if key == 'environments':
                self.environments = [Environment(**env) for env in kwargs[key]]
            else:
                setattr(self, key, kwargs.get(key, None))

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

