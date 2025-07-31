from sqlalchemy import text, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, BigInteger, String, Text, Boolean, DateTime, ForeignKey, Float
)

Base = declarative_base()

class CarrierContactModel(Base):
    __tablename__ = "carriers_contacts"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True)
    organization_id = Column(Integer)
    operational_unit_id = Column(Integer)
    status = Column(String(10))
    code = Column(UUID, nullable=False, server_default=text("uuid_generate_v4()"))
    company_name = Column(Text, nullable=False)
    company_tax_type = Column(Integer)
    company_tax_number = Column(String(30))
    company_email = Column(String(200))
    company_phone = Column(String(50))
    company_mobile = Column(String(50))
    source = Column(String(10), nullable=False)
    country = Column(String(2))
    is_critical = Column(Boolean, default=False)
    contact_name = Column(String(200))
    contact_email = Column(String(100))
    trucks = Column(Integer)
    pwd = Column(String(100))
    carrier_id = Column(Integer)
    old_id = Column(UUID)
    old_uuid = Column(String(50))
    old_ref_id = Column(UUID)
    old_uid = Column(String(100))
    old_created_at = Column(DateTime(timezone=True))
    old_updated_at = Column(DateTime(timezone=True))
    is_deleted = Column(Boolean, server_default="false", nullable=False)

class CarrierContactLogModel(Base):
    __tablename__ = "carriers_contacts_logs"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True)
    contact_id = Column(BigInteger, ForeignKey("platform.carriers_contacts.id"), nullable=False)
    changes = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_by = Column(Integer)
    deleted_at = Column(DateTime(timezone=True))
    deleted_by = Column(Integer)

class CarrierContactCommentModel(Base):
    __tablename__ = "carriers_contacts_comments"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True)
    contact_id = Column(BigInteger, ForeignKey("platform.carriers_contacts.id"), nullable=False)
    comments = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_by = Column(Integer)
    deleted_at = Column(DateTime(timezone=True))
    deleted_by = Column(Integer)

class CarriersContactsAddressModel(Base):
    __tablename__ = "carriers_contacts_address"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    contact_id = Column(BigInteger, ForeignKey("platform.carriers_contacts.id"), nullable=False)
    code = Column(UUID, nullable=False, server_default=text("uuid_generate_v4()"))
    status = Column(String(10))
    place_id = Column(String, nullable=True)
    formatted_address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address_components = Column(JSONB, nullable=False)
    country = Column(String, nullable=True)
    province = Column(String, nullable=True)
    address_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
