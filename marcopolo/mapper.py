def generate_target_map(polos):
    target_map = {}
    for polo in polos:
        for target in polo._targets:
            target_map[target] = polo
    return target_map

def map_dependency(polos, target_map):
    not_found = {}
    for polo in polos:
        for env in polo.environments:
            for (idx, dep) in enumerate(env.dependencies):
                found_dep = target_map.get(dep, None)
                if found_dep is None:
                    not_found[dep] = { 'polo': polo, 'env': env }
                else:
                    env.dependencies[idx] = found_dep
    return not_found

def generate_dependency_list(polos):
    dep_list = {}
    for polo in polos:
        for env in polo.environments:
            for dep in env.dependencies:
                dep_list[dep] = env
    return (dep_list)

