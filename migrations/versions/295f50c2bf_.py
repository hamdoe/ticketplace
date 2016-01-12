"""Data migration for content's genre, location, status

Warning!!! This will break when model script changes.


The correct script should create a table independent of current models script(the declarative model).
Suggestion by Elmer from #sqlalchemy (Thanks a lot!)

Will adapt when time comes... probably... hopefully...

```
T_CONTENT = sa.Table(
    'content',
    sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('genre', sa.Text))

def upgrade()

  .. change type of `genre` column ..
  con = op.get_bind()
  params = []
  for row in con.execute(T_CONTENT.select()).fetchall():
    params.append({
        'genre': new_genre_content(content.genre),
        'content_id': content.id})
  content_update = T_CONTENT.update().values(
      value=sa.bindparam('genre')).where(
          T_CONTENT.c.id == sa.bindparam('content_id'))
  con.execute(content_update, params)
```


Revision ID: 295f50c2bf
Revises: 537bb869081
Create Date: 2016-01-08 17:09:48.999577

"""

WARNING_MESSAGE = 'Warning! This migration script might break in the future. See %s for details.' % __file__

# revision identifiers, used by Alembic.
from alembic import op
from ticketplace.models import Content, db

revision = '295f50c2bf'
down_revision = '537bb869081'


def upgrade_genre(genre):
    return {
        '0': '연극',
        '1': '뮤지컬',
        '2': '아동/가족'
    }[genre]


def downgrade_genre(genre):
    return {
        '연극': '0',
        '뮤지컬': '1',
        '아동/가족': '2'
    }[genre]


def upgrade_location(location):
    return {
        '0': '서울',
        '1': '경기',
        '2': '기타'
    }[location]


def downgrade_location(location):
    return {
        '서울': '0',
        '경기': '1',
        '기타': '2'
    }[location]


def upgrade_status(status):
    return {
        '1': '준비중',
        '2': '판매중',
        '3': '아동/판매종료'
    }[status]


def downgrade_status(status):
    return {
        '준비중': '1',
        '판매중': '2',
        '아동/판매종료': '3'
    }[status]


def upgrade():
    op.execute('COMMIT')  # Prevent hanging when upgrading multiple at once
    print(WARNING_MESSAGE)
    for content in Content.query.all():
        content.genre = upgrade_genre(content.genre)
    db.session.commit()


def downgrade():
    op.execute('COMMIT')
    print(WARNING_MESSAGE)
    for content in Content.query.all():
        content.genre = downgrade_genre(content.genre)
    db.session.commit()
