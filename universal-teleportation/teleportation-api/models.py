"""
WekezaOmniOS Teleportation API Models
Defines the Pydantic schemas for the high-level orchestration of process migration.
"""

from pydantic import BaseModel, Field

class TeleportRequest(BaseModel):
    """
    Schema for a high-level environment-to-environment migration request.
    This model acts as the primary 'Order' for the UAT engine.
    """
    process_id: int = Field(..., description="The unique Process Identifier (PID) to be migrated.")
    source_env: str = Field(..., description="The identifier of the source environment (e.g., 'ubuntu-dev').")
    target_env: str = Field(..., description="The identifier of the target environment (e.g., 'windows-test').")

    class Config:
        json_schema_extra = {
            "example": {
                "process_id": 1921,
                "source_env": "ubuntu-dev",
                "target_env": "windows-test"
            }
        }

class TeleportResponse(BaseModel):
    """
    Standardized response schema for orchestration acknowledgment.
    """
    status: str = Field(..., description="The outcome of the request (e.g., 'success', 'failed').")
    message: str = Field(..., description="A detailed human-readable description of the operation status.")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Process 1921 teleportation started."
            }
        }
