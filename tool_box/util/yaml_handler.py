
import yaml
import collections

def load(f):
    def construct_odict(loader, node):
        return collections.OrderedDict(loader.construct_pairs(node))

    yaml.add_constructor(u'tag:yaml.org,2002:map', construct_odict)
    data = yaml.load(f.read().decode('utf-8'))

    return data

def dump(data, f):
    def represent_odict(dumper, instance):
         return dumper.represent_mapping(u'tag:yaml.org,2002:map', instance.items())

    yaml.add_representer(collections.OrderedDict, represent_odict)
    yaml.dump(
        data,
        f,
        default_flow_style=False,
        encoding='utf-8',
        allow_unicode=True
        )


