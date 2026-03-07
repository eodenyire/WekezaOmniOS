"""
WekezaOmniOS Environment Loader
Rehydrates the process environment context from captured metadata.
"""

import json
import os

def load_environment(env_file):
    """
    Reads environment variables from a JSON file and injects them 
    into the current execution context.
    
    Args:
        env_file (str): Path to the env.json file within the snapshot.
    """
    # 1. Check for file existence
    if not os.path.exists(env_file):
        print(f"[Environment Loader] WARNING: No environment file found at {env_file}. Proceeding with default system environment.")
        return

    try:
        # 2. Parse the captured environment variables
        with open(env_file, "r") as f:
            env_vars = json.load(f)
        
        # 3. Inject variables into the local OS environment
        # This ensures the restored process sees its original config
        for key, value in env_vars.items():
            os.environ[key] = str(value)
            
        print(f"[Environment Loader] SUCCESS: {len(env_vars)} variables loaded from {env_file}")

    except json.JSONDecodeError:
        print(f"[Environment Loader] ERROR: Failed to parse {env_file}. File may be corrupted.")
    except Exception as e:
        print(f"[Environment Loader] UNEXPECTED ERROR: {str(e)}")
