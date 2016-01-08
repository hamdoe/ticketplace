"""Schema migration for content

Revision ID: 295f50c2bf
Revises: 537bb869081
Create Date: 2016-01-08 17:09:48.999577

"""

# revision identifiers, used by Alembic.
from ticketplace.models import Content, db

revision = '295f50c2bf'
down_revision = '537bb869081'

def upgrade_genre(genre):
    return ['연극', '뮤지컬', '아동/가족'][int(genre)]


def downgrade_genre(genre):
    return {
        '연극': '0',
        '뮤지컬': '1',
        '아동/가족': '2'
    }[genre]


def upgrade():
    for content in Content.query.all():
        content.genre = upgrade_genre(content.genre)
    db.session.commit()


def downgrade():
    for content in Content.query.all():
        content.genre = downgrade_genre(content.genre)
    db.session.commit()