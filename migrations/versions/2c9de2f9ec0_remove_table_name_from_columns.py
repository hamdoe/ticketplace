"""Remove table name from columns

Revision ID: 2c9de2f9ec0
Revises: 44bea7299a8
Create Date: 2015-12-29 14:05:21.739612

"""

# revision identifiers, used by Alembic.
revision = '2c9de2f9ec0'
down_revision = '44bea7299a8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('user')
    op.alter_column('company', 'id', new_column_name='username')
    op.alter_column('company', 'company_id', new_column_name='id')
    op.alter_column('company', 'company_name', new_column_name='name')
    op.alter_column('company', 'company_type', new_column_name='type')
    op.alter_column('content', 'content_id', new_column_name='id')

    op.drop_constraint('content_company_id_fkey', 'content', type_='foreignkey')
    op.create_foreign_key('content_company_id_fkey', 'content', 'company', ['company_id'], ['id'])
    op.drop_constraint('tag_association_content_id_fkey', 'tag_association', type_='foreignkey')
    op.create_foreign_key('tag_association_content_id_fkey', 'tag_association', 'content', ['content_id'], ['id'])


def downgrade():
    # Caution: Order of name altering and setting of foreign key is important
    # since the name of the primary key is changing
    op.drop_constraint('tag_association_content_id_fkey', 'tag_association', type_='foreignkey')
    op.create_foreign_key('tag_association_content_id_fkey', 'tag_association', 'content', ['content_id'], ['id'])
    op.drop_constraint('content_company_id_fkey', 'content', type_='foreignkey')
    op.create_foreign_key('content_company_id_fkey', 'content', 'company', ['company_id'], ['id'])

    op.alter_column('company', 'id', new_column_name='company_id')
    op.alter_column('company', 'username', new_column_name='id')
    op.alter_column('company', 'name', new_column_name='company_name')
    op.alter_column('company', 'type', new_column_name='company_type')
    op.alter_column('content', 'id', new_column_name='content_id')

    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    ### end Alembic commands ###
