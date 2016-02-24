import sys
import json

import yaml

from jinja2 import Template

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
                 'tier' ]

    def __init__(self, **kwargs):
        for key in self.__keys__:
            setattr(self, key, kwargs.get(key, None))

    def _serialize(self):
        out = {
            'aliases': [str(x) for x in self.aliases],
            'datacenters': self.datacenters,
            'dependencies': self.dependencies,
            'infrastructure': self.infrastructure,
            'tier': self.tier
        }
        if self.default:
            out['default'] = True
        return out

    def set_name(self, parent, name=None, template=None):
        self.__name_template = template
        if name is None and template is not None:
            self.name = Template(template).render(
                    **dict(parent.__dict__.items()+self.__dict__.items()))
        else:
            self.name = name

class Polo(SerializableObject):
    # XXX These are the keys expected in schema_version 0.0.1,
    #         we use this list to confirm data coming in
    __keys__ = [ 'aliases',
                 'description',
                 'name',
                 'owner',
                 'schema_version',
                 'source',
                 'summary',
                 'tracker',
                 'website' ]

    def __init__(self, **kwargs):
        self._targets = []
        for key in self.__keys__:
            setattr(self, key, kwargs.get(key, None))
        self._targets.append(self.name)
        self._targets.extend(self.aliases)
        self.environments = []
        for e in kwargs.get('environments', {}):
            env = Environment(**e)
            env.set_name(self, template=kwargs['environment_name_template'])
            self._targets.append(env.name)
            self._targets.extend(env.aliases)
            self.environments.append(env)

    def _serialize(self):
        out = {}
        for x in self.__keys__:
            out[x] = getattr(self, x)
        out['environments'] = []
        for x in self.environments:
            out['environments'].append(x._serialize())
        return [out]

def parse(data):
    data = yaml.load(data)
    return Polo(**data[0])
