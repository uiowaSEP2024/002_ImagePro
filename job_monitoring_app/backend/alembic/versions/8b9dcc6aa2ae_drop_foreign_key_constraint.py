"""drop_foreign_key_constraint

Revision ID: 8b9dcc6aa2ae
Revises: 156cc0e79869
Create Date: 2024-04-04 21:47:57.845037

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "8b9dcc6aa2ae"
down_revision = "156cc0e79869"
branch_labels = None
depends_on = None


def upgrade():
    # Drop foreign key constraint study_configs -> users
    op.drop_constraint("study_configurations_provider_id_fkey", "study_configurations")

    # Add foreign key constraint study_configs -> providers
    op.create_foreign_key(
        "study_configurations_provider_id_provider_table_fkey",
        "study_configurations",
        "providers",
        ["provider_id"],
        ["id"],
    )

    # Drop foreign key constraint studies -> users (provider role)
    op.drop_constraint("studies_provider_id_fkey", "studies")

    # Add foreign key constraint studies -> providers
    op.create_foreign_key(
        "studies_provider_id_provider_table_fkey",
        "studies",
        "providers",
        ["provider_id"],
        ["id"],
    )

    # Drop foreign key constraint studies -> users (hospital role)
    op.drop_constraint("studies_hospital_id_fkey", "studies")

    # Add foreign key constraint studies -> hospitals
    op.create_foreign_key(
        "studies_hospital_id_hospital_table_fkey",
        "studies",
        "hospitals",
        ["hospital_id"],
        ["id"],
    )

    # Add foreign key constraint user_providers -> providers
    op.create_foreign_key(
        "user_provider_provider_id_fkey",
        "user_provider",
        "providers",
        ["provider_id"],
        ["id"],
    )

    # Add foreign key constraint user_hospitals -> hospital
    op.create_foreign_key(
        "user_hospital_hospital_id_fkey",
        "user_hospital",
        "hospitals",
        ["hospital_id"],
        ["id"],
    )


def downgrade():
    # Add foreign key constraint study_configs -> users
    op.create_foreign_key(
        "study_configurations_provider_id_fkey",
        "study_configurations",
        "users",
        ["provider_id"],
        ["id"],
    )

    # Drop foreign key constraint study_configs -> providers
    op.drop_constraint(
        "study_configurations_provider_id_provider_table_fkey", "study_configurations"
    )

    # Add foreign key constraint studies -> users (provider role)
    op.create_foreign_key(
        "studies_provider_id_fkey", "studies", "users", ["provider_id"], ["id"]
    )

    # Drop foreign key constraint studies -> providers
    op.drop_constraint("studies_provider_id_provider_table_fkey", "studies")

    # Add foreign key constraint studies -> users (hospital role)
    op.create_foreign_key(
        "studies_hospital_id_fkey", "studies", "users", ["hospital_id"], ["id"]
    )

    # Drop foreign key constraint studies -> hospitals
    op.drop_constraint("studies_hospital_id_hospital_table_fkey", "studies")

    # Drop foreign key constraint user_providers -> providers
    op.drop_constraint("user_provider_provider_id_fkey", "user_provider")

    # Drop foreign key constraint user_hospitals -> hospitals
    op.drop_constraint("user_hospital_hospital_id_fkey", "user_hospital")
