"""empty message

Revision ID: 2d6221a53fbe
Revises: None
Create Date: 2015-05-14 11:32:38.733813

"""

# revision identifiers, used by Alembic.
revision = '2d6221a53fbe'
down_revision = None


from alembic import op
import sqlalchemy as sa
from abovl import utils


def upgrade():
    op.create_table('oauth_client',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('token', sa.String(length=40)),
        sa.Column('refresh_token', sa.String(length=40)),
        sa.Column('client_id', sa.String(length=40)),
        sa.Column('client_secret', sa.String(length=80)),
        sa.Column('ratelimit', sa.Float()),
        sa.Column('expire_in', utils.UTCDateTime),
        sa.Column('created', utils.UTCDateTime, default=utils.now),
        sa.Column('scopes', sa.Text()),
        sa.Column('username', sa.String(length=512)),
        
        sa.Index('ix_token', 'token')
    )

def downgrade():
    op.drop_table('oauth_client')
