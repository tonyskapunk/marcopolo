def parse_schema_file():
    print parse(open(sys.argv[1], 'r').read()).to_yaml()
