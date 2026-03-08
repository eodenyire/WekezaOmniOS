"""Teleport controller for Phase 2 cross-node orchestration."""

import datetime
import importlib.util
import os


def _load_module(name, path):
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

capture_manager_module = _load_module(
	"capture_manager", os.path.join(BASE_DIR, "state-capture", "capture_manager.py")
)
snapshot_builder_module = _load_module(
	"snapshot_builder", os.path.join(BASE_DIR, "snapshot-engine", "snapshot_builder.py")
)
transfer_manager_module = _load_module(
	"transfer_manager", os.path.join(BASE_DIR, "transfer-layer", "transfer_manager.py")
)
node_controller_module = _load_module(
	"node_controller", os.path.join(BASE_DIR, "api", "node_controller.py")
)
telemetry_module = _load_module(
	"node_telemetry", os.path.join(BASE_DIR, "monitoring", "node_telemetry.py")
)

CaptureManager = capture_manager_module.CaptureManager
build_snapshot = snapshot_builder_module.build_snapshot
TransferManager = transfer_manager_module.TransferManager
NodeController = node_controller_module.NodeController
NodeTelemetry = telemetry_module.NodeTelemetry


class TeleportController:
	def __init__(self):
		self.capture_manager = CaptureManager(snapshot_dir=os.path.join(BASE_DIR, "snapshots"))
		self.transfer_manager = TransferManager(snapshot_dir=os.path.join(BASE_DIR, "snapshots"))
		self.node_controller = NodeController()
		self.telemetry = NodeTelemetry(telemetry_file=os.path.join(BASE_DIR, "logs", "node_telemetry.jsonl"))

	def teleport_remote(self, process_id, target_node_id, protocol="auto"):
		tracking_id = f"phase2-{process_id}-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

		target_node = self.node_controller.get_node(target_node_id)
		if not target_node:
			raise ValueError(f"target node not found: {target_node_id}")

		# 1) capture
		info = self.capture_manager.capture_process(process_id)

		# 2) build tar snapshot
		source_dir = os.path.join(BASE_DIR, "snapshots", f"process_{process_id}")
		artifact_name = f"remote_{tracking_id}.tar.gz"
		artifact_path = os.path.join(BASE_DIR, "snapshots", artifact_name)
		metadata = {
			"tracking_id": tracking_id,
			"process_id": process_id,
			"target_node_id": target_node_id,
			"target_address": target_node.get("address"),
			"created_at": datetime.datetime.utcnow().isoformat() + "Z",
		}
		ok = build_snapshot(source_dir, artifact_path, metadata)
		if not ok:
			raise RuntimeError("failed to build snapshot artifact")

		# 3) transfer
		transfer_result = self.transfer_manager.send_snapshot(
			process_id=process_id,
			target_path=os.path.join(BASE_DIR, "snapshots", "remote-inbox"),
			target_host=target_node.get("address", "127.0.0.1"),
			protocol=protocol,
		)

		self.telemetry.emit(
			"remote_teleport",
			{
				"tracking_id": tracking_id,
				"process_id": process_id,
				"target_node_id": target_node_id,
				"transfer": transfer_result,
				"process_info": info,
			},
		)

		return {
			"status": "success",
			"tracking_id": tracking_id,
			"target_node_id": target_node_id,
			"transfer_protocol": transfer_result.get("protocol", protocol),
			"snapshot_artifact": artifact_path,
		}

