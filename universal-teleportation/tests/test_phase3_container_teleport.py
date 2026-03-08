import os
import importlib.util


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


teleport_controller_module = load_module(
    "teleport_controller", os.path.join(BASE_DIR, "api", "teleport_controller.py")
)
node_controller_module = load_module(
    "node_controller", os.path.join(BASE_DIR, "api", "node_controller.py")
)


def test_phase3_container_teleport_simulated():
    # Ensure local node exists in registry for target resolution.
    node_controller = node_controller_module.NodeController()
    node_controller.register("phase3-local", "127.0.0.1", role="controller", port=8000)

    controller = teleport_controller_module.TeleportController()
    result = controller.teleport_container(
        container_id="demo-container",
        target_node_id="phase3-local",
        protocol="local",
        runtime="auto",
        checkpoint_name="phase3-checkpoint",
    )

    assert result["status"] == "success"
    assert result["container_id"] == "demo-container"
    assert result["target_node_id"] == "phase3-local"
    assert result["checkpoint_name"] == "phase3-checkpoint"
    assert result["transfer_protocol"] in ("local", "auto")
