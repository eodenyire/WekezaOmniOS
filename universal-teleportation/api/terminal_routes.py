"""
API routes for the WekezaOmniOS Integrated Terminal (WebSocket).
"""
import asyncio
import pty
import os
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/ws/terminal")
async def terminal_websocket(websocket: WebSocket):
    """
    Handles the WebSocket connection for the integrated terminal.
    Spawns a pseudo-terminal (pty) and relays data between it and the client.
    """
    await websocket.accept()
    
    # Create a new pseudo-terminal
    master_fd, slave_fd = pty.openpty()
    
    # Start a shell process (e.g., bash) in the pseudo-terminal
    # The process will run in the project's root directory
    process = await asyncio.create_subprocess_shell(
        'bash',
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        cwd="/workspaces/WekezaOmniOS/universal-teleportation"
    )
    
    # Coroutine to read from the pty and send to the client
    async def read_from_pty():
        try:
            while True:
                data = os.read(master_fd, 1024)
                if not data:
                    break
                await websocket.send_text(data.decode(errors='ignore'))
        except (WebSocketDisconnect, OSError):
            pass
        finally:
            # Clean up when the connection is closed
            if process.returncode is None:
                process.kill()
            os.close(master_fd)
            os.close(slave_fd)

    # Coroutine to read from the client and write to the pty
    async def write_to_pty():
        try:
            while True:
                data = await websocket.receive_text()
                os.write(master_fd, data.encode())
        except (WebSocketDisconnect, OSError):
            pass

    # Run both coroutines concurrently
    read_task = asyncio.create_task(read_from_pty())
    write_task = asyncio.create_task(write_to_pty())
    
    done, pending = await asyncio.wait(
        {read_task, write_task},
        return_when=asyncio.FIRST_COMPLETED,
    )

    # Cancel any pending tasks to ensure cleanup
    for task in pending:
        task.cancel()
