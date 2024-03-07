from sqlalchemy.orm import Session
from app import models, schemas


def create_pacs(db: Session, pacs: schemas.PacsCreate) -> models.Pacs:
    """
    Creates a new PACS in the database.

    Args:
        db (Session): The database session.
        PACS (schemas.PacsCreate): The Pacs to create.
    """

    db_pacs = models.Pacs(pacs_name=pacs.pacs_name, hospital_id=pacs.hospital_id)
    db.add(db_pacs)
    db.commit()
    db.refresh(db_pacs)
    return db_pacs
