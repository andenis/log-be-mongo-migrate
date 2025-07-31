from sqlalchemy import (Column, Integer, String, Text, Boolean, ForeignKey, DateTime)
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class CatalogResourceModel(Base):
    __tablename__ = "catalog_resources"
    __table_args__ = {"schema": "common"}

    id = Column(Integer, primary_key=True)
    code = Column(Text, nullable=False, unique=True)
    key_code = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True)
    parent_id = Column(Integer, ForeignKey("common.catalog_resources.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    created_by = Column(Text, nullable=True)
    updated_by = Column(Text, nullable=True)
    deleted_by = Column(Text, nullable=True)

    abbreviation = Column(Text, nullable=True)
    old_parent = Column(Text, nullable=True)
    old_catalog_type = Column(Text, nullable=True)

    catalog_type_id = Column(Integer, ForeignKey("common.catalog_types.id"), nullable=False)
    parent_ref = Column(String(30), nullable=True)
