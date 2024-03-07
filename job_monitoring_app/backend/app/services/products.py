from sqlalchemy.orm import Session
from app import models, schemas


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """
    Creates a new product in the database.

    Args:
        db (Session): The database session.
        product (schemas.ProductCreate): The product to create.
    """

    db_product = models.Product(
        product_name=product.product_name, provider_id=product.provider_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
