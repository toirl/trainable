"""Use trainable specific profiles

Revision ID: e7a82496755d
Revises: 3b1d44cdad56
Create Date: 2016-10-26 12:43:25.961835

"""

# revision identifiers, used by Alembic.
revision = 'e7a82496755d'
down_revision = '3b1d44cdad56'

from alembic import op
import sqlalchemy as sa


INSERTS = """
UPDATE modules set clazzpath = 'trainable.model.user.TrainableUser' where id = 3;
UPDATE modules set clazzpath = 'trainable.model.user.TrainableProfile' where id = 6;
"""
DELETES = """
UPDATE modules set clazzpath = 'ringo.model.user.Profile' where id = 6;
UPDATE modules set clazzpath = 'ringo.model.user.User' where id = 3;
"""


def iter_statements(stmts):
    for st in [x for x in stmts.split('\n') if x]:
        op.execute(st)


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('strava_access_key', sa.String(), nullable=True))
    op.add_column('profiles', sa.Column('strava_client_id', sa.String(), nullable=True))
    ### end Alembic commands ###
    iter_statements(INSERTS)


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles', 'strava_client_id')
    op.drop_column('profiles', 'strava_access_key')
    ### end Alembic commands ###
    iter_statements(DELETES)