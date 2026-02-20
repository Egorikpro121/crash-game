"""WebSocket routes for real-time game updates."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List
import json
import asyncio
from datetime import datetime

from src.game.engine.game_session import GameSession
from src.database.connection import get_db

router = APIRouter()


class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        """Initialize connection manager."""
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """
        Connect a WebSocket.
        
        Args:
            websocket: WebSocket connection
            user_id: User ID
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_connections[user_id] = websocket
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """
        Disconnect a WebSocket.
        
        Args:
            websocket: WebSocket connection
            user_id: User ID
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id in self.user_connections:
            del self.user_connections[user_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        Send message to specific connection.
        
        Args:
            message: Message data
            websocket: WebSocket connection
        """
        await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        """
        Broadcast message to all connections.
        
        Args:
            message: Message data
        """
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        
        # Remove disconnected connections
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)


manager = ConnectionManager()


@router.websocket("/ws/game")
async def websocket_game(websocket: WebSocket, user_id: int):
    """
    WebSocket endpoint for game updates.
    
    Args:
        websocket: WebSocket connection
        user_id: User ID
    """
    await manager.connect(websocket, user_id)
    
    try:
        # Send initial connection confirmation
        await manager.send_personal_message({
            "type": "connected",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)
        
        # Start game update loop
        db = next(get_db())
        game_session = GameSession(db)
        
        while True:
            # Get round status
            status = game_session.get_round_status()
            
            # Send update
            await manager.send_personal_message({
                "type": "round_update",
                "data": status
            }, websocket)
            
            # Wait before next update
            await asyncio.sleep(0.1)  # 10 updates per second
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        manager.disconnect(websocket, user_id)
        print(f"WebSocket error: {e}")


async def broadcast_round_update(update_data: dict):
    """
    Broadcast round update to all connected clients.
    
    Args:
        update_data: Update data
    """
    await manager.broadcast({
        "type": "round_update",
        "data": update_data,
        "timestamp": datetime.utcnow().isoformat()
    })


async def broadcast_crash(multiplier: float):
    """
    Broadcast crash event.
    
    Args:
        multiplier: Crash multiplier
    """
    await manager.broadcast({
        "type": "crash",
        "multiplier": multiplier,
        "timestamp": datetime.utcnow().isoformat()
    })
