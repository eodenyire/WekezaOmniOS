"""Unified container runtime adapter for Phase 2."""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from docker_adapter import DockerAdapter
from containerd_adapter import ContainerdAdapter


class ContainerAdapter:
    def __init__(self):
        self.docker = DockerAdapter()
        self.containerd = ContainerdAdapter()

    def detect_runtime(self):
        if self.docker.is_available():
            return "docker"
        if self.containerd.is_available():
            return "containerd"
        return None

    def list_containers(self):
        runtime = self.detect_runtime()
        if runtime == "docker":
            return runtime, self.docker.list_containers()
        if runtime == "containerd":
            return runtime, self.containerd.list_containers()
        return None, []

    def checkpoint_container(self, container_id, checkpoint_name="uat-checkpoint"):
        runtime = self.detect_runtime()
        if runtime == "docker":
            return self.docker.checkpoint(container_id, checkpoint_name)
        if runtime == "containerd":
            return self.containerd.checkpoint(container_id, checkpoint_name)
        return False, "no container runtime available"

    def restore_container(self, container_id, checkpoint_name="uat-checkpoint"):
        runtime = self.detect_runtime()
        if runtime == "docker":
            return self.docker.restore(container_id, checkpoint_name)
        if runtime == "containerd":
            return self.containerd.restore(container_id, checkpoint_name)
        return False, "no container runtime available"
