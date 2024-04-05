from app import models

from app.schemas import PacsCreate
from app.services.pacs import create_pacs


def test_create_pacs(db):
    # Create a new hospital

    hospital = models.Hospital(hospital_name="test_hospital")
    db.add(hospital)
    db.commit()
    db.refresh(hospital)

    # Create a new PACS

    db_pacs = create_pacs(
        db,
        PacsCreate.parse_obj(
            {
                "pacs_name": "test_pacs",
                "hospital_id": hospital.id,
            }
        ),
    )

    assert db_pacs.pacs_name == "test_pacs"
    assert db_pacs.hospital_id == hospital.id
    assert db_pacs.created_at is not None

    assert len(hospital.pacs) == 1
    assert db_pacs.hospital.id == hospital.id
