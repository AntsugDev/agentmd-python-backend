"""Settings management routes."""

from fastapi import APIRouter, Depends, HTTPException

from agentmd.api.dependencies import verify_config, verify_session
from agentmd.config import config_manager

router = APIRouter()


@router.get("/settings")
async def get_settings(
    _: None = Depends(verify_session),
    __: None = Depends(verify_config),
):
    config = config_manager.to_dict()
    return {
        "modelSelected": config.get("model_selected"),
        "lastUpdated": config.get("last_updated"),
        "providers": config.get("providers"),
    }


@router.get("/settings/model")
async def get_selected_model(
    _: None = Depends(verify_session),
    __: None = Depends(verify_config),
):
    return {"modelSelected": config_manager.get_model_selected()}


@router.put("/settings/{provider}")
async def update_provider_apikey(
    provider: str,
    body: dict,
    _: None = Depends(verify_session),
    __: None = Depends(verify_config),
):
    providers = config_manager.get_providers()
    if provider not in providers:
        raise HTTPException(status_code=404, detail=f"Provider {provider} not found")

    if "apikey" not in body or not isinstance(body["apikey"], str):
        raise HTTPException(status_code=400, detail="Bad request")

    provider_config = config_manager.get_provider_config(provider) or {}
    provider_config["api_key"] = body["apikey"]
    config_manager.set_provider_config(provider, provider_config)

    return {"status": "success", "message": f"API key updated for {provider}"}


@router.delete("/settings/{provider}")
async def delete_provider_apikey(
    provider: str,
    _: None = Depends(verify_session),
    __: None = Depends(verify_config),
):
    providers = config_manager.get_providers()
    if provider not in providers:
        raise HTTPException(status_code=404, detail=f"Provider {provider} not found")

    config_manager.clear_provider_apikey(provider)
    return {"status": "success", "message": f"API key deleted for {provider}"}
