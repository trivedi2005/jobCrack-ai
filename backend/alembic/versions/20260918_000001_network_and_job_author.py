"""Add user connections and job authors."""

from alembic import op
import sqlalchemy as sa

revision = "20260918_network_jobs"
down_revision = "20260917_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    if "connections" not in inspector.get_table_names():
        op.create_table(
            "connections",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("requester_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
            sa.Column("recipient_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
            sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(timezone=True)),
            sa.UniqueConstraint("requester_id", "recipient_id"),
        )
    columns = {column["name"] for column in inspector.get_columns("jobs")}
    if "posted_by_id" not in columns:
        op.add_column("jobs", sa.Column("posted_by_id", sa.Integer(), nullable=True))
        op.create_foreign_key("fk_jobs_posted_by_id_users", "jobs", "users", ["posted_by_id"], ["id"], ondelete="SET NULL")


def downgrade() -> None:
    op.drop_constraint("fk_jobs_posted_by_id_users", "jobs", type_="foreignkey")
    op.drop_column("jobs", "posted_by_id")
    op.drop_table("connections")
