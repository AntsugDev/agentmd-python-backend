"""AI models listing and management routes."""

from fastapi import APIRouter, Depends

from agentmd.api.dependencies import verify_config, verify_session
from agentmd.config import config_manager

router = APIRouter()


@router.get("/models")
async def get_models(
    _: None = Depends(verify_session),
    __: None = Depends(verify_config),
):
    models = []
    providers_config = config_manager.to_dict().get("providers", {})

    for provider_name, provider_config in providers_config.items():
        if provider_config and "models" in provider_config:
            for model in provider_config["models"]:
                model_name = model.get("name") if isinstance(model, dict) else model.name
                display_name = model.get("display_name", model_name) if isinstance(model, dict) else (model.display_name or model_name)
                models.append({
                    "value": f"{provider_name}|{model_name.replace('models/', '')}",
                    "text": f"{provider_name} - {display_name}",
                })

    models.append({"value": "no-limits", "text": "No Limits"})
    return models


@router.get("/select_models/{model}")
async def select_model(
    model: str,
    _: None = Depends(verify_session),
    __: None = Depends(verify_config),
):
    config_manager.set_model_selected(model)
    return {"status": "success", "message": f"Model {model} selected"}


@router.get("/sincro")
async def synchronize_models(
    _: None = Depends(verify_session),
    __: None = Depends(verify_config),
):
    return {
        "status": "success",
        "message": "La sincronizzazione è stata avviata con successo.",
    }
