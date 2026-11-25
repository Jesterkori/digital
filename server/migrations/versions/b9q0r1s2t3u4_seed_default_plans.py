"""seed default membership plans

A brand-new database (e.g. a fresh Render Postgres) has an empty `plans`
table, so the Membership page has nothing to choose from. This inserts the
same four default plans as app/scripts/seed_plans.py. Plans that already
exist (matched by name) are left untouched.

Revision ID: b9q0r1s2t3u4
Revises: a8p9q0r1s2t3
Create Date: 2026-11-25 00:00:00.000000

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b9q0r1s2t3u4'
down_revision: Union[str, None] = 'a8p9q0r1s2t3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEFAULT_PLANS = [
    ("base", "Base", "Perfect for individuals starting their credit journey", 0.0, 10, 2),
    ("royal", "Royal", "For growing businesses needing better credit management", 4999.0, 20, 5),
    ("groups", "Groups", "For organizations and groups managing multiple entities", 14999.0, 50, 15),
    ("enterprise", "Enterprise", "Custom solutions for large enterprises", 0.0, 999, 999),
]


def upgrade() -> None:
    conn = op.get_bind()
    insert = sa.text(
        """
        INSERT INTO plans (id, name, display_name, description, duration_type,
                           price, validity_days, follow_up_limit,
                           legal_assistance_limit, is_active, created_at, updated_at)
        VALUES (:id, :name, :display_name, :description, 'monthly',
                :price, 365, :follow_up_limit,
                :legal_assistance_limit, TRUE, now(), now())
        ON CONFLICT (name) DO NOTHING
        """
    )
    for name, display_name, description, price, follow_ups, legal in DEFAULT_PLANS:
        conn.execute(insert, {
            "id": str(uuid.uuid4()),
            "name": name,
            "display_name": display_name,
            "description": description,
            "price": price,
            "follow_up_limit": follow_ups,
            "legal_assistance_limit": legal,
        })


def downgrade() -> None:
    # Plans may have subscriptions attached by now; leave them in place.
    pass
