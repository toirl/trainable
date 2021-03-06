"""Added action to sync a activity with strava

Revision ID: 7e910ab38f9c
Revises: cd16bf2b6eba
Create Date: 2016-11-10 19:40:35.318643

"""

# revision identifiers, used by Alembic.
revision = '7e910ab38f9c'
down_revision = 'cd16bf2b6eba'

from alembic import op
import sqlalchemy as sa


INSERTS = """
INSERT INTO actions (id, mid, name, url, icon, description, bundle, display, permission) VALUES (46, 1000, 'Sync', 'syncstrava/{id}', 'fa fa-refresh', '', false, '', 'update');
"""
DELETES = """
DELETE FROM actions WHERE id = 46;
"""


def iter_statements(stmts):
    for st in [x for x in stmts.split('\n') if x]:
        op.execute(st)


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###
    iter_statements(INSERTS)


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###
    iter_statements(DELETES)
