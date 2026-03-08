"""
WekezaOmniOS Monitoring Tests — Node Telemetry
"""
import pytest
from monitoring.node_telemetry import NodeTelemetry, TelemetryRecord
from monitoring.resource_monitor import ResourceMonitor
from monitoring.telemetry_hub import TelemetryHub


# ------ NodeTelemetry ------

def test_node_telemetry_record():
    nt = NodeTelemetry("node-1")
    sample = nt.record(cpu_pct=25.0, memory_pct=40.0, throughput_mbps=100.0)
    assert isinstance(sample, TelemetryRecord)
    assert sample.node_id == "node-1"


def test_node_telemetry_latest():
    nt = NodeTelemetry("node-2")
    nt.record(30.0, 50.0)
    nt.record(40.0, 60.0)
    latest = nt.latest()
    assert latest.cpu_pct == 40.0


def test_node_telemetry_latest_empty():
    nt = NodeTelemetry("node-empty")
    assert nt.latest() is None


def test_node_telemetry_average():
    nt = NodeTelemetry("node-avg")
    nt.record(10.0, 20.0)
    nt.record(30.0, 40.0)
    avg = nt.average()
    assert avg["avg_cpu_pct"] == 20.0
    assert avg["avg_memory_pct"] == 30.0


def test_node_telemetry_history():
    nt = NodeTelemetry("node-hist")
    nt.record(5.0, 10.0)
    h = nt.history()
    assert len(h) == 1
    assert "timestamp" in h[0]


def test_telemetry_record_success_rate():
    nt = NodeTelemetry("node-sr")
    nt.record(20.0, 30.0, teleport_success=8, teleport_failure=2)
    d = nt.latest().to_dict()
    assert d["success_rate"] == pytest.approx(0.8)


# ------ ResourceMonitor ------

def test_resource_monitor_instantiation():
    monitor = ResourceMonitor()
    assert monitor is not None


def test_resource_monitor_get_stats():
    monitor = ResourceMonitor()
    stats = monitor.get_system_stats()
    assert "cpu" in stats
    assert "memory" in stats
    assert 0 <= stats["cpu"] <= 100
    assert 0 <= stats["memory"] <= 100


# ------ TelemetryHub ------

def test_telemetry_hub_log_event():
    hub = TelemetryHub()
    hub.log_event("TestModule", "INFO", "Test message")
    assert len(hub.events) == 1
    assert hub.events[0]["module"] == "TestModule"


def test_telemetry_hub_export(tmp_path):
    hub = TelemetryHub()
    hub.log_event("CaptureEngine", "SUCCESS", "Snapshot created")
    report_path = str(tmp_path / "telemetry.json")
    hub.export_telemetry(report_path)
    import json
    with open(report_path) as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["type"] == "SUCCESS"
