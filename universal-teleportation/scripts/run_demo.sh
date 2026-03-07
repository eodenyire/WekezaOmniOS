python demo_app.py &

PID=$!

python cli/teleport.py capture $PID
