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


def get_hospital_users(db: Session, hospital_id: int) -> models.User:
    """
    Get all users in a hospital.

    Args:
        db (Session): The database session.
        hospital_id (int): The hospital id.
    """
    return (
        db.query(models.User)
        .join(models.HospitalUsers)
        .filter(models.HospitalUsers.hospital_id == hospital_id)
        .all()
    )


def get_all_hospitals(db: Session) -> models.Hospital:
    """
    Get all hospitals in the database.

    Args:
        db (Session): The database session.
    """
    return db.query(models.Hospital).all()


def get_hospital_by_id(db: Session, hospital_id: int) -> models.Hospital:
    """
    Get a hospital by id.

    Args:
        db (Session): The database session.
        hospital_id (int): The hospital id.
    """
    return db.query(models.Hospital).get(hospital_id)


def get_hospital_by_user_id(db: Session, user_id: int) -> models.Hospital:
    """
    Get a hospital by a user id.

    Args:
        db (Session): The database session.
        user_id (int): The user id.
    """
    hospital_user = (
        db.query(models.HospitalUsers)
        .filter(models.HospitalUsers.user_id == user_id)
        .first()
    )
    if hospital_user:
        return get_hospital_by_id(db, hospital_user.hospital_id)
    return None
