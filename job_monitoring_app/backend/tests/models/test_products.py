from app import models

from app.schemas import ProductCreate
from app.services.products import create_product


def test_create_products(db):
    # Create a new provider

    provider = models.Provider(provider_name="test_provider")
    db.add(provider)
    db.commit()
    db.refresh(provider)

    # Create a new product

    db_product = create_product(
        db,
        ProductCreate.parse_obj(
            {
                "product_name": "test_product",
                "provider_id": provider.id,
            }
        ),
    )

    assert db_product.product_name == "test_product"
    assert db_product.provider_id == provider.id
    assert db_product.created_at is not None

    assert len(provider.products) == 1
    assert db_product.provider.id == provider.id
