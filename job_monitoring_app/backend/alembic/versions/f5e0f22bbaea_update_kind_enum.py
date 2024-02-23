from alembic import op

# revision identifiers, used by Alembic
revision = "f5e0f22bbaea"
down_revision = "8c4f7aee9b55"
branch_labels = None
depends_on = None


def upgrade():
    # Drop the new enum type
    op.execute("DROP TYPE IF EXISTS event_kind CASCADE;")

    # Create the old enum type
    op.execute(
        "CREATE TYPE event_kind AS ENUM ('In progress', 'Pending', 'Complete','Error','Info');"
    )

    # Alter the table to add the 'kind' column with the old enum type
    op.execute("ALTER TABLE events ADD COLUMN kind event_kind;")

    # Update null values to a default value
    op.execute("UPDATE events SET kind = 'In progress' WHERE kind IS NULL;")

    # Then make the column required
    op.execute("ALTER TABLE events ALTER COLUMN kind SET NOT NULL;")


def downgrade():
    # Drop the new enum type
    op.execute("DROP TYPE IF EXISTS event_kind CASCADE;")

    # Create the old enum type
    op.execute("CREATE TYPE event_kind AS ENUM ('step', 'complete', 'info', 'error');")

    # Alter the table to add the 'kind' column with the old enum type
    op.execute("ALTER TABLE events ADD COLUMN kind event_kind;")
