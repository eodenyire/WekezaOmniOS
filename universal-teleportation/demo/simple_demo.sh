#!/bin/bash
# Simple Practical Demo: Develop on Linux, Test on All Platforms

clear
cat << 'EOF'
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🚀 WekezaOmniOS - PRACTICAL APPLICATION TELEPORTATION DEMO    ║
║                                                                  ║
║   Scenario: You're developing a web app on Linux,               ║
║             but want to see how it looks on Windows, Android,   ║
║             iOS, and Cloud platforms                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

EOF

echo "Current Platform: $(uname -s) ($(uname -m))"
echo ""

# Start the demo app
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 1: Your Application Running on Linux"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Starting your demo web app on port 8080..."

python3 demo/my_app.py &
APP_PID=$!
sleep 2

echo "✅ App is running on http://localhost:8080 (PID: $APP_PID)"
echo ""
echo "📱 Open this URL in your browser to see it: http://localhost:8080"
echo "   You'll see: Platform detection, system info, and a beautiful UI"
echo ""
echo "Press ENTER to continue to cross-platform simulation..."
read

# Show cross-platform testing
cat << 'EOF'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: How Your App Would Look on Different Platforms
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The teleportation engine adapts your app for each platform:

┌──────────────────────────────────────────────────────────────┐
│ 🪟 WINDOWS                                                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Your app would show:                                         │
│   Platform: Windows 11                                       │
│   Path: C:\Users\YourName\Desktop\my_app.py                │
│   URL: http://localhost:8080                                 │
│                                                              │
│ Adaptations made:                                            │
│   ✓ Linux paths → Windows paths (/ → C:\)                   │
│   ✓ POSIX signals → Windows events                          │
│   ✓ File permissions → Windows ACLs                         │
│   ✓ UI renders with Windows fonts & colors                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 🤖 ANDROID                                                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Your app would show:                                         │
│   Platform: Android 14                                       │
│   Path: /data/local/tmp/my_app.py                           │
│   URL: http://localhost:8080                                 │
│                                                              │
│ Adaptations made:                                            │
│   ✓ Responsive mobile layout (touch-friendly)               │
│   ✓ Android filesystem structure                            │
│   ✓ Runs in Termux/Pydroid environment                      │
│   ✓ Mobile browser optimizations                            │
│   ✓ Portrait/landscape auto-adjustment                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 🍎 iOS / macOS                                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Your app would show:                                         │
│   Platform: iOS 17 / macOS Sonoma                            │
│   Path: /Applications/MyApp.app/Contents/my_app.py          │
│   URL: http://localhost:8080                                 │
│                                                              │
│ Adaptations made:                                            │
│   ✓ Apple HIG-compliant UI design                           │
│   ✓ macOS/iOS filesystem sandbox                            │
│   ✓ Touch gestures (swipe, pinch, tap)                      │
│   ✓ Dark mode support (iOS style)                           │
│   ✓ Notch-safe area for modern iPhones                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ ☁️  CLOUD (AWS/GCP/Azure)                                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Your app would run on:                                       │
│   Platform: Amazon Linux 2 (AWS EC2)                         │
│   Region: us-east-1                                          │
│   URL: http://ec2-52-12-34-56.compute-1.amazonaws.com:8080  │
│                                                              │
│ Deployment includes:                                         │
│   ✓ Auto-scaling group (min:1, max:10)                      │
│   ✓ Load balancer (Application LB)                          │
│   ✓ CloudWatch monitoring                                    │
│   ✓ S3 snapshot storage                                      │
│   ✓ SSL certificate (HTTPS)                                 │
│   ✓ Global CDN (CloudFront)                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘

EOF

read -p "Press ENTER to see how to use the API commands..."

# Show API usage
cat << EOF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: How to Actually Teleport Your App
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Here are the actual commands you would use:

1️⃣  CAPTURE your running app:
   ────────────────────────────────────────────────────────────
   curl -X POST http://localhost:8000/capture \\
     -H "Content-Type: application/json" \\
     -d '{
       "process_id": $APP_PID,
       "include_memory": true,
       "include_files": true
     }'

2️⃣  REGISTER target platforms (one-time setup):
   ────────────────────────────────────────────────────────────
   # Windows machine
   curl -X POST http://localhost:8000/nodes/register \\
     -d '{"node_id":"windows-pc","address":"192.168.1.100","port":8000,"role":"windows-runtime"}'
   
   # Android device
   curl -X POST http://localhost:8000/nodes/register \\
     -d '{"node_id":"android-phone","address":"192.168.1.101","port":8000,"role":"android-runtime"}'
   
   # Cloud server
   curl -X POST http://localhost:8000/nodes/register \\
     -d '{"node_id":"aws-prod","address":"ec2.amazonaws.com","port":8000,"role":"cloud"}'

3️⃣  TELEPORT to target platform:
   ────────────────────────────────────────────────────────────
   curl -X POST http://localhost:8000/teleport/remote \\
     -d '{
       "source_snapshot_id": "snapshot-$APP_PID",
       "target_node_id": "windows-pc",
       "transfer_protocol": "ssh"
     }'

4️⃣  CHECK running applications on all platforms:
   ────────────────────────────────────────────────────────────
   curl http://localhost:8000/nodes
   
   # Shows all registered nodes and their status

5️⃣  CONTAINERIZE and deploy everywhere:
   ────────────────────────────────────────────────────────────
   # Create container checkpoint
   curl -X POST http://localhost:8000/container/checkpoint \\
     -d '{"container_id":"my-app","runtime":"docker"}'
   
   # Deploy to any platform
   curl -X POST http://localhost:8000/teleport/container \\
     -d '{"container_id":"my-app","target_node_id":"aws-prod"}'

EOF

echo ""
read -p "Press ENTER to see the CLI tool..."

# Show CLI usage
cat << 'EOF'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4: Using the CLI (easier than curl commands!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The CLI tool makes it even easier:

📦 Install CLI:
   $ cd cli/
   $ chmod +x teleport.py

🚀 Basic Usage:
   
   #Capture current app
   $ ./teleport.py capture --pid $APP_PID
   
   # List target platforms
   $ ./teleport.py list-nodes
   
   # Teleport to Windows
   $ ./teleport.py send --target windows-pc --snapshot snapshot-$APP_PID
   
   # Teleport to Android
   $ ./teleport.py send --target android-phone --snapshot snapshot-$APP_PID
   
   # Teleport to cloud
   $ ./teleport.py send --target aws-prod --snapshot snapshot-$APP_PID --cloud

💡 Interactive Mode:
   $ ./teleport.py
   
   This starts an interactive shell where you can:
   • See available commands
   • Tab-complete node names
   • View real-time teleportation progress
   • Monitor running apps across platforms

EOF

echo ""
read -p "Press ENTER for practical workflow example..."

# Practical example
cat << EOF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5: Practical Daily Workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scenario: You're developing a web app and need to test on all platforms

Monday Morning:
──────────────
1. Start developing on Linux:
   $ python3 my_app.py
   $ # Make changes, test locally

2. Snapshot your app:
   $ ./teleport.py capture --pid \$(pgrep -f my_app.py)
   ✅ Snapshot created: snapshot-12345

3. Test on Windows:
   $ ./teleport.py send --target windows-pc --snapshot snapshot-12345
   ✅ App teleported to Windows
   🌐 View at: http://192.168.1.100:8080

4. Test on mobile (Android):
   $ ./teleport.py send --target android-phone --snapshot snapshot-12345
   ✅ App teleported to Android
   📱 View on phone: http://192.168.1.101:8080

5. Deploy to production (AWS):
   $ ./teleport.py send --target aws-prod --snapshot snapshot-12345 --cloud
   ✅ Deployed to AWS
   🌍 Public URL: https://myapp.example.com

All in under 5 minutes! 🎉

EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ DEMO COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Your demo app is still running at: http://localhost:8080"
echo "PID: $APP_PID"
echo ""
echo "To stop it: kill $APP_PID"
echo ""
echo "Next steps:"
echo "  1. Open http://localhost:8080 in your browser"
echo "  2. Try the CLI commands above"
echo "  3. Read docs/README.md for more details"
echo "  4. Explore the API at http://localhost:8000"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
