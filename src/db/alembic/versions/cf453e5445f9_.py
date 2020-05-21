"""empty message

Revision ID: cf453e5445f9
Revises: 
Create Date: 2020-05-22 00:03:53.346188

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cf453e5445f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('names',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('local_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id', 'local_uuid', name=op.f('pk__names')),
    sa.UniqueConstraint('local_uuid', name=op.f('uq__names__local_uuid'))
    )
    op.create_table('parsed_company',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('link_guid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ogrn', sa.Integer(), nullable=True),
    sa.Column('inn', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('status_date', sa.DateTime(), nullable=True),
    sa.Column('primary_names_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['primary_names_uuid'], ['names.local_uuid'], name=op.f('fk__parsed_company__primary_names_uuid__names')),
    sa.PrimaryKeyConstraint('id', 'link_guid', name=op.f('pk__parsed_company')),
    sa.UniqueConstraint('link_guid', name=op.f('uq__parsed_company__link_guid')),
    sa.UniqueConstraint('status_date', name=op.f('uq__parsed_company__status_date'))
    )
    op.create_table('parsed_event',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('guid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('data_publish', sa.DateTime(), nullable=True),
    sa.Column('is_annuled', sa.Boolean(), nullable=True),
    sa.Column('is_locked', sa.Boolean(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('publisher_name', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('publisher_type', sa.String(), nullable=False),
    sa.Column('bankrupt_name', sa.String(), nullable=False),
    sa.Column('is_refuted', sa.Boolean(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('primary_link_guid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['primary_link_guid'], ['parsed_company.link_guid'], name=op.f('fk__parsed_event__primary_link_guid__parsed_company')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__parsed_event')),
    sa.UniqueConstraint('data_publish', name=op.f('uq__parsed_event__data_publish'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parsed_event')
    op.drop_table('parsed_company')
    op.drop_table('names')
    # ### end Alembic commands ###
