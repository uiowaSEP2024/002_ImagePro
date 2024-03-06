from config import config

from app.schemas import ProviderCreate
from app.services.providers import create_provider


def test_provider_creation():
    db = config.db.SessionLocal()
    db_provider = create_provider(
        db,
        ProviderCreate.parse_obj(
            {
                "provider_name": "test_provider",
            }
        ),
    )

    assert db_provider.provider_name == "test_provider"
    assert db_provider.created_at is not None
