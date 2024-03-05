from config import config

from app.schemas import HospitalCreate
from app.services.hospitals import create_hospital


def test_hospital_creation():
    db = config.db.SessionLocal()
    db_hospital = create_hospital(
        db,
        HospitalCreate.parse_obj(
            {
                "hospital_name": "test_hospital",
            }
        ),
    )

    assert db_hospital.hospital_name == "test_hospital"
    assert db_hospital.created_at is not None
