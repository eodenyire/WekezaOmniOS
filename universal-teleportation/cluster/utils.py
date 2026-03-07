"""
WekezaOmniOS Cluster Utilities
"""

def validate_node_name(name):
    """Ensures node names are URL and filesystem friendly."""
    if not name or len(name) < 3:
        raise ValueError("Node name must be at least 3 characters long.")
    return name.strip().lower().replace(" ", "-")

def generate_node_id(name):
    """Generates a standardized ID for the registry."""
    clean_name = validate_node_name(name)
    return f"node_{clean_name}"
