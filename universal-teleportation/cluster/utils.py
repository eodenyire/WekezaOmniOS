def validate_node_name(name):
    if not name:
        raise ValueError("Node name cannot be empty")
    return name

def generate_node_id(name):
    return f"node_{name.lower()}"
