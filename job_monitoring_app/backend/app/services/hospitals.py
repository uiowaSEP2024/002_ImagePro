from sqlalchemy.orm import Session
from app import models, schemas


def create_hospital(db: Session, hospital: schemas.HospitalCreate) -> models.Hospital:
    """
    Creates a new hospital in the database.

    Args:
        db (Session): The database session.
        hospital (schemas.HospitalCreate): The hospital to create.
    """

    db_hospital = models.Hospital(hospital_name=hospital.hospital_name)
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital
