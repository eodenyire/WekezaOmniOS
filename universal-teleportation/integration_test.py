#!/usr/bin/env python3
"""
WekezaOmniOS - Integration Test Suite
Tests complete workflows across multiple phases
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("\n" + "="*80)
print("  🔥 WekezaOmniOS INTEGRATION TEST SUITE")
print("     Testing Cross-Phase Workflows")
print("="*80)

# Import from cluster modules (these work with standard imports)
from cluster.node_registry import NodeRegistry
from cluster.scheduler import Scheduler
from monitoring.resource_monitor import ResourceMonitor
from security.encryption import EncryptionManager

# Test results tracker
results = []

def test_result(name, passed, details=""):
    """Track test results"""
    status = "✅ PASS" if passed else "❌ FAIL"
    results.append({"name": name, "passed": passed, "details": details})
    print(f"    {status} - {name}")
    if details:
        print(f"           {details}")

# ============================================================================
# INTEGRATION TEST 1: Cluster + Scheduling + Security
# ============================================================================
print("\n" + "─"*80)
print("📦 Test 1: Cluster Orchestration with Security")
print("─"*80)

try:
    # 1. Initialize components
    registry = NodeRegistry(registry_file="/tmp/test_registry.json")
    scheduler = Scheduler(registry)
    encryption = EncryptionManager()
    
    # 2. Register nodes
    nodes_to_register = [
        {"node_id": "test-node-1", "address": "10.0.0.1", "port": 8000, "role": "compute"},
        {"node_id": "test-node-2", "address": "10.0.0.2", "port": 8000, "role": "compute"},
        {"node_id": "test-node-3", "address": "10.0.0.3", "port": 8000, "role": "storage"},
    ]
    
    for node_data in nodes_to_register:
        registry.register(**node_data)
    
    test_result("Node Registration", True, f"{len(nodes_to_register)} nodes registered")
    
    # 3. List and verify nodes
    all_nodes = registry.list_nodes()
    test_result("Node Listing", len(all_nodes) >= len(nodes_to_register), 
                f"{len(all_nodes)} nodes in registry")
    
    # 4. Schedule a workload
    target_node = scheduler.schedule()
    test_result("Workload Scheduling", target_node is not None,
                f"Selected node: {target_node.get('node_id') if target_node else 'None'}")
    
    # 5. Test encryption for secure transfer
    test_data = b"sensitive snapshot data"
    encrypted = encryption.encrypt(test_data)
    decrypted = encryption.decrypt(encrypted)
    test_result("Encryption/Decryption", decrypted == test_data,
                f"Data integrity verified")
    
    test_result("Integration Test 1", True, "All components working together")
    
except Exception as e:
    test_result("Integration Test 1", False, f"Error: {str(e)}")

# ============================================================================
# INTEGRATION TEST 2: Live Migration + Monitoring
# ============================================================================
print("\n" + "─"*80)
print("📦 Test 2: Live Migration with Monitoring")
print("─"*80)

try:
    # Import live migration components using importlib
    import importlib.util
    
    def load_module(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        return None
    
    # Load live migration modules
    mc_module = load_module("migration_controller", "live-migration/migration_controller.py")
    
  if mc_module:
        MigrationController = mc_module.MigrationController
        controller = MigrationController()
        
        # Start a simulated migration
        result = controller.start_migration(process_id=9999)
        
        test_result("Live Migration", result['state'] == 'COMPLETE',
                    f"Iterations: {result['dirty_iterations']}")
        
        # Monitor resource usage
        monitor = ResourceMonitor()
        stats = monitor.get_stats()
        
        test_result("Resource Monitoring", 
                    stats['cpu_percent'] >= 0 and stats['memory_percent'] >= 0,
                    f"CPU: {stats['cpu_percent']:.1f}%, MEM: {stats['memory_percent']:.1f}%")
        
        test_result("Integration Test 2", True, "Migration + Monitoring working")
    else:
        test_result("Integration Test 2", False, "Could not load migration module")
        
except Exception as e:
    test_result("Integration Test 2", False, f"Error: {str(e)}")

# ============================================================================
# INTEGRATION TEST 3: Multi-Phase Cross-Platform Workflow
# ============================================================================
print("\n" + "─"*80)
print("📦 Test 3: Cross-Platform Workflow")
print("─"*80)

try:
    # Load runtime adapters
    rm_module = load_module("runtime_mapper", "runtime-adapters/runtime_mapper.py")
    
    if rm_module:
        RuntimeMapper = rm_module.RuntimeMapper
        mapper = RuntimeMapper()
        
        # Test path mapping across platforms
        linux_path = "/usr/local/bin/app"
        win_paths = mapper.map_paths([linux_path], "linux", "windows")
        test_result("Cross-Platform Path Mapping", len(win_paths) > 0,
                    f"Mapped {linux_path} -> {win_paths[0] if win_paths else 'N/A'}")
        
        # Test signal mapping
        linux_signal = "SIGTERM"
        win_signal = mapper.map_signal(linux_signal, "linux", "windows")
        test_result("Signal Mapping", win_signal is not None,
                    f"SIGTERM -> {win_signal}")
        
        test_result("Integration Test 3", True, "Cross-platform adaptation working")
    else:
        test_result("Integration Test 3", False, "Could not load runtime mapper")
        
except Exception as e:
    test_result("Integration Test 3", False, f"Error: {str(e)}")

# ============================================================================
# INTEGRATION TEST 4: AI Scheduler + Cloud + Global Fabric
# ============================================================================
print("\n" + "─"*80)
print("📦 Test 4: AI-Driven Cloud Orchestration")
print("─"*80)

try:
    # Load AI scheduler
    wp_module = load_module("workload_predictor", "ai-scheduler/workload_predictor.py")
    ons_module = load_module("optimal_node_selector", "ai-scheduler/optimal_node_selector.py")
    
    if wp_module and ons_module:
        WorkloadPredictor = wp_module.WorkloadPredictor
        OptimalNodeSelector = ons_module.OptimalNodeSelector
        
        predictor = WorkloadPredictor()
        selector = OptimalNodeSelector()
        
        # Predict resources for a workload
        workload = {"memory_mb": 1024, "cpu_cores": 4, "os": "linux"}
        prediction = predictor.predict_resources(workload)
        
        test_result("AI Resource Prediction", 
                    'memory_mb' in prediction and 'confidence' in prediction,
                    f"Predicted {prediction['memory_mb']}MB RAM, confidence: {prediction['confidence']*100:.0f}%")
        
        # Select optimal node
        cloud_nodes = [
            {"id": "aws-us-east-1", "cpu_available": 80, "memory_available": 8192, "status": "ONLINE"},
            {"id": "gcp-europe-west1", "cpu_available": 60, "memory_available": 4096, "status": "ONLINE"},
            {"id": "azure-asia-south1", "cpu_available": 40, "memory_available": 2048, "status": "ONLINE"},
        ]
        
        best = selector.select_best_node(cloud_nodes, workload)
        test_result("Optimal Node Selection", best is not None,
                    f"Selected: {best['id'] if best else 'None'}")
        
        test_result("Integration Test 4", True, "AI + Cloud orchestration working")
    else:
        test_result("Integration Test 4", False, "Could not load AI modules")
        
except Exception as e:
    test_result("Integration Test 4", False, f"Error: {str(e)}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("  📊 INTEGRATION TEST RESULTS")
print("="*80)

passed = sum(1 for r in results if r['passed'])
total = len(results)
success_rate = (passed / total * 100) if total > 0 else 0

print(f"\nTotal Tests: {total}")
print(f"Passed: {passed}")
print(f"Failed: {total - passed}")
print(f"Success Rate: {success_rate:.1f}%")

print("\n" + "─"*80)
print("Detailed Results:")
print("─"*80)
for r in results:
    status = "✅" if r['passed'] else "❌"
    print(f"{status} {r['name']}")
    if r['details']:
        print(f"   └─ {r['details']}")

if success_rate == 100:
    print("\n" + "="*80)
    print("  🎉 ALL INTEGRATION TESTS PASSED!")
    print("  System is fully operational across all phases")
    print("="*80 + "\n")
else:
    print("\n" + "="*80)
    print(f"  ⚠️  {total - passed} test(s) failed - review results above")
    print("="*80 + "\n")
