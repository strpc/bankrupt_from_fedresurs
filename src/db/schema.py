from sqlalchemy import (
    Column, ForeignKey, Integer,
    MetaData, String, Table, DateTime, Boolean, BigInteger
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

names_table = Table(
    'names',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('name', String, nullable=False),
    Column(
        'local_uuid', UUID(as_uuid=True),
        primary_key=True, nullable=False, unique=True
        ),
    Column('date', DateTime(timezone=True), server_default=func.now()),
)

parse_company_table = Table(
    'parsed_company',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('link_guid', UUID(as_uuid=True), nullable=False),
    Column('ogrn', BigInteger),
    Column('inn', BigInteger),
    Column('name', String, nullable=False),
    Column('address', String, nullable=False),
    Column('status', String, nullable=False),
    Column('status_date', DateTime),
    Column('primary_names_uuid', UUID(as_uuid=True), ForeignKey('names.local_uuid')),
)

parse_event_table = Table(
    'parsed_event',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('guid', UUID(as_uuid=True), nullable=False),
    Column('number', BigInteger),
    Column('data_publish', DateTime),
    Column('is_annuled', Boolean, nullable=True),
    Column('is_locked', Boolean, nullable=True),
    Column('title', String, nullable=False),
    Column('publisher_name', String, nullable=False),
    Column('type', String, nullable=False),
    Column('publisher_type', String, nullable=False),
    Column('bankrupt_name', String, nullable=False),
    Column('is_refuted', Boolean, nullable=False),
    Column('text', String),
    Column('primary_link_guid', Integer, ForeignKey('parsed_company.id')),
)
