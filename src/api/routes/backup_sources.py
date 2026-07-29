from fastapi import APIRouter

from src.services.configuration_service import ConfigurationService

router = APIRouter(
    prefix="/api/backup-sources",
    tags=["Backup Sources"]
)

configuration_service = ConfigurationService()


@router.get("")
def get_backup_sources():

    config = configuration_service.load()
    backup = config["backup"]
    
    return  {
    "standard": backup.get("standard_sources", []),
    "custom": backup.get("custom_sources", [])
}