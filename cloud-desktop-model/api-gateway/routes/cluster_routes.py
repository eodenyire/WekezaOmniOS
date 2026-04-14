"""
Cluster / node management routes — register, list, remove nodes, and
inspect cluster health and resource usage.
"""

from fastapi import APIRouter, Depends, HTTPException

from ..schemas.models import ClusterStatusResponse, NodeRegisterRequest, NodeResponse
from ..middleware.auth_middleware import get_current_user_id

router = APIRouter(prefix="/cluster", tags=["Cluster"])

_control_plane = None


def set_control_plane(cp) -> None:
    global _control_plane
    _control_plane = cp


def _cp():
    if _control_plane is None:
        raise HTTPException(status_code=503, detail="Control plane not initialised")
    return _control_plane


@router.post("/nodes", response_model=NodeResponse, status_code=201)
def register_node(request: NodeRegisterRequest,
                  _uid: str = Depends(get_current_user_id)):
    """Register a new compute node with the cluster."""
    try:
        node = _cp().add_node(
            node_id=request.node_id,
            node_type=request.node_type,
            address=request.address,
            cpu_cores=request.cpu_cores,
            ram_gb=request.ram_gb,
        )
        return node
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/nodes", summary="List registered nodes")
def list_nodes(node_type: str = None, status: str = None,
               _uid: str = Depends(get_current_user_id)):
    nodes = _cp().list_nodes(node_type=node_type, status=status)
    return {"status": "ok", "count": len(nodes), "nodes": nodes}


@router.delete("/nodes/{node_id}", summary="Remove a node")
def remove_node(node_id: str, _uid: str = Depends(get_current_user_id)):
    removed = _cp().remove_node(node_id)
    if not removed:
        raise HTTPException(status_code=404, detail=f"Node not found: {node_id}")
    return {"status": "removed", "node_id": node_id}


@router.get("/nodes/{node_id}/health", summary="Check node health")
def node_health(node_id: str, _uid: str = Depends(get_current_user_id)):
    result = _cp().node_health(node_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Node not found: {node_id}")
    return result


@router.get("/health", summary="Full cluster health")
def cluster_health(_uid: str = Depends(get_current_user_id)):
    nodes = _cp().cluster_health()
    usage = _cp().resource_usage()
    return {
        "status": "ok",
        "total_nodes": len(nodes),
        "resource_usage": usage,
        "nodes": nodes,
    }


@router.get("/resources", summary="Resource usage summary")
def resource_usage(_uid: str = Depends(get_current_user_id)):
    return _cp().resource_usage()
