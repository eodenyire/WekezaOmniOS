"""
WekezaOmniOS State Capture Utilities
Helper functions for managing directories and paths during process state dumping.
"""

import os

def ensure_dir(path: str):
    """
    Ensures that a directory exists at the given path.
    If the path does not exist, it creates the directory (including parent directories).
    
    Args:
        path (str): The directory path to verify or create.
    """
    if not os.path.exists(path):
        try:
            # exist_ok=True prevents race conditions if the dir is created simultaneously
            os.makedirs(path, exist_ok=True)
            print(f"[Utils] SUCCESS: Created directory structure: {path}")
        except PermissionError:
            print(f"[Utils] ERROR: Permission denied. Cannot create directory: {path}")
            raise
        except Exception as e:
            print(f"[Utils] ERROR: Failed to create directory {path}. Reason: {e}")
            raise
    else:
        # Directory already exists; no action needed.
        pass
