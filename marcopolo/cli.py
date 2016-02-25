import sys
from objects import parse

def parse_schema_file(input=None):
    if input is None:
        input = sys.argv[1]
    polo = parse(open(input, 'r').read())
    print polo.to_yaml()
    return polo
