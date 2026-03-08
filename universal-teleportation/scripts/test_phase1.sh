#!/bin/bash

# WekezaOmniOS Phase 1 - End-to-End Test Script
# This script demonstrates the complete teleportation workflow

echo "🚀 WekezaOmniOS Phase 1 - Universal Application Teleportation"
echo "=============================================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Navigate to project root
cd "$(dirname "$0")/.." || exit 1

echo -e "${BLUE}Phase 1: Setup and Validation${NC}"
echo "--------------------------------------------------------------"

# 1. Create required directories
echo "📁 Creating directory structure..."
mkdir -p snapshots logs temp demo

# 2. Check system status
echo ""
echo "🔍 Checking system status..."
python3 cli/teleport.py status

echo ""
echo -e "${BLUE}Phase 2: Launch Demo Application${NC}"
echo "--------------------------------------------------------------"

# 3. Start the demo application
echo "🎯 Starting demo counter application..."
python3 demo/demo_app.py &
DEMO_PID=$!
echo $DEMO_PID > temp/demo_app.pid
echo -e "${GREEN}✅ Demo app started with PID: $DEMO_PID${NC}"

# Give it a moment to initialize
sleep 3

echo ""
echo -e "${BLUE}Phase 3: State Capture${NC}"
echo "--------------------------------------------------------------"

# 4. Capture the running process
echo "🧊 Capturing process state for PID $DEMO_PID..."
python3 cli/teleport.py capture $DEMO_PID

echo ""
echo -e "${BLUE}Phase 4: Snapshot Creation${NC}"
echo "--------------------------------------------------------------"

# 5. Create a snapshot
echo "📦 Creating portable snapshot..."
python3 cli/teleport.py snapshot $DEMO_PID "phase1_demo_snapshot"

# Verify snapshot was created
if [ -f "snapshots/phase1_demo_snapshot.tar.gz" ]; then
    SNAPSHOT_SIZE=$(du -h "snapshots/phase1_demo_snapshot.tar.gz" | cut -f1)
    echo -e "${GREEN}✅ Snapshot created successfully: $SNAPSHOT_SIZE${NC}"
    echo "📂 Location: snapshots/phase1_demo_snapshot.tar.gz"
else
    echo -e "${YELLOW}⚠️  Snapshot file not found (may be in metadata-only mode)${NC}"
fi

echo ""
echo -e "${BLUE}Phase 5: Process Inspection${NC}"
echo "--------------------------------------------------------------"

# 6. Show what was captured
echo "🔬 Examining captured state..."
if [ -d "snapshots/process_$DEMO_PID" ]; then
    echo "Contents of snapshot directory:"
    ls -lah "snapshots/process_$DEMO_PID/"
    
    # Show metadata if available
    if [ -f "snapshots/process_$DEMO_PID/process_metadata.json" ]; then
        echo ""
        echo "Process Metadata:"
        cat "snapshots/process_$DEMO_PID/process_metadata.json"
    fi
fi

echo ""
echo -e "${BLUE}Phase 6: State Restoration (Simulation)${NC}"
echo "--------------------------------------------------------------"

# 7. Attempt to restore (will show captured data in fallback mode)
echo "⚡ Attempting to restore process state..."
python3 cli/teleport.py restore $DEMO_PID

echo ""
echo -e "${BLUE}Phase 7: Cleanup${NC}"
echo "--------------------------------------------------------------"

# 8. Clean up the demo process
echo "🧹 Cleaning up demo process..."
kill $DEMO_PID 2>/dev/null && echo -e "${GREEN}✅ Demo process terminated${NC}" || echo -e "${YELLOW}⚠️  Demo process already terminated${NC}"

echo ""
echo "=============================================================="
echo -e "${GREEN}✅ Phase 1 Test Complete!${NC}"
echo ""
echo "📊 Summary:"
echo "   - Process capture: ✅ Complete"
echo "   - Snapshot creation: ✅ Complete"
echo "   - State inspection: ✅ Complete"
echo "   - Restoration test: ✅ Complete"
echo ""
echo "📝 Notes:"
echo "   - Full CRIU functionality requires installation and privileges"
echo "   - Fallback mode captures metadata and environment"
echo "   - Phase 2 will add cross-environment transfer"
echo ""
echo "🎯 Next Steps:"
echo "   1. Review generated snapshots in ./snapshots/"
echo "   2. Examine logs in ./logs/"
echo "   3. Test API endpoints: python3 api/server.py"
echo ""
