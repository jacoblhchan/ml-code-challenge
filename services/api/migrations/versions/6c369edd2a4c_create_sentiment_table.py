"""Create Sentiment table

Revision ID: 6c369edd2a4c
Revises: 
Create Date: 2020-02-27 04:08:22.170132

"""
from alembic import op
from sqlalchemy import Column, func, Integer, String, Text, Float, TIMESTAMP

# revision identifiers, used by Alembic.
revision = '6c369edd2a4c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    sentiment_table = op.create_table('sentiment',
                    Column('id', Integer, primary_key=True),
                    Column('sentiment_score', Float(2,4), nullable=False),
                    Column('confidence', Float(2,4), nullable=False),
                    Column('sentence', Text, nullable=False),
                    Column('created_on', TIMESTAMP, nullable=False, server_default=func.now()),
                    Column('updated_on', TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now()),
                    )

    # This type of data is not necessary for the application to work. It shouldn't be
    #  added as part of a migration. This is merely for convenience.
    op.bulk_insert(sentiment_table, [
        {'sentiment_score': 0.8, 'sentence': "has a film used manhattan 's architecture in such a gloriously goofy way . ", 'confidence': 0.99 },
        {'sentiment_score': -0.01, 'sentence': 'that worked five years ago but has since lost its fizz ', 'confidence': 0.94 },
        {'sentiment_score': 0.9, 'sentence': 'prove that movie-star intensity can overcome bad hair design ', 'confidence': 0.96 }
    ])


def downgrade():
    op.drop_table('sentiment')
