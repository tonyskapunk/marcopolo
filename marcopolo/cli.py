import os
import sys
from objects import parse

def parse_schema_file(input=None):
    if input is None:
        input = os.environ.get('POLO_FILE')
    polo = parse(open(input, 'r').read())
    print(polo.to_yaml())
    return polo
