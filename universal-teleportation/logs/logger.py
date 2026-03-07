# 📄 logger.py
# This is the "pen" that writes to your "Black Box." Instead of using print(), all modules will import this to ensure logs are time-stamped and categorized.
"""
WekezaOmniOS Logging Utility
Standardizes the audit trail for all teleportation events.
"""

import logging
import os
from datetime import datetime

# Ensure the logs directory exists
LOG_DIR = os.path.dirname(os.path.abspath(__file__))

def get_logger(name, log_file, level=logging.INFO):
    """Function to setup as many loggers as you want"""
    handler = logging.FileHandler(os.path.join(LOG_DIR, log_file))        
    handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s', 
                                         datefmt='%Y-%m-%d %H:%M:%S'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Pre-defined loggers for the core engine
capture_logger = get_logger('CAPTURE', 'capture.log')
restore_logger = get_logger('RESTORE', 'restore.log')
teleport_logger = get_logger('TELEPORT', 'teleport.log')

def log_event(category, message, pid=None):
    """High-level helper to log an event across the system."""
    pid_str = f"[PID:{pid}] " if pid else ""
    full_message = f"{pid_str}{message}"
    
    if category == "CAPTURE":
        capture_logger.info(full_message)
    elif category == "RESTORE":
        restore_logger.info(full_message)
    
    # All major events go to the master teleport log
    teleport_logger.info(f"[{category}] {full_message}")
    print(f"[{category}] {full_message}") # Still print to console for Phase 1 CLI
