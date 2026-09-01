
def load_dict_query(path):
    queries = {}
    with open(path, "r") as f:
        content = f.read()
    sections = content.split("-- ")

    for section in sections[1:]:
        line = section.strip().split("\n", 1)
        name = line[0].strip()
        sql = line[1].strip()
        queries[name] = sql

    return queries
