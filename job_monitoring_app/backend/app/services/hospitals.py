from sqlalchemy.orm import Session
from app import models, schemas
from app.models.hospital_users import hospital_user_association


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


def get_hospital_users(db: Session, hospital_id: int) -> models.User:
    """
    Get all users in a hospital.

    Args:
        db (Session): The database session.
        hospital_id (int): The hospital id.
    """
    return (
        db.query(models.User)
        .join(hospital_user_association)
        .filter(hospital_user_association.c.hospital_id == hospital_id)
        .all()
    )
