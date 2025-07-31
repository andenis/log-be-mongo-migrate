from sqlalchemy import (
    Column, BigInteger, Integer, String, Boolean, Text, DateTime, ForeignKey, Float, CHAR
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB
import sqlalchemy as sa

Base = declarative_base()

class CarrierModel(Base):
    __tablename__ = "carriers"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(UUID(as_uuid=True), unique=True, nullable=False, server_default=sa.text("uuid_generate_v4()"))
    status = Column(String(20))
    doc_status = Column(String(20))
    company_name = Column(Text, nullable=False)
    company_tax_type = Column(Integer, nullable=False)
    company_tax_number = Column(String(30), nullable=False)
    company_email = Column(String(200), nullable=True)
    company_phone = Column(String(50))
    company_mobile = Column(String(50), nullable=True)
    country = Column(CHAR(2), nullable=False)
    is_critical = Column(Boolean, nullable=False, server_default=sa.text('FALSE'))
    admin_accounting_code = Column(String(50))
    admin_note = Column(Text, nullable=True)
    carrier_contact_id = Column(Integer, nullable=True)
    old_id = Column(String(50), unique=True)
    old_sap_card_code = Column(String(100))
    old_created_at = Column(DateTime(timezone=True))
    old_updated_at = Column(DateTime(timezone=True))
    is_deleted = Column(Boolean, nullable=False, server_default=sa.text("FALSE"))
    organization_id = Column(Integer, nullable=False)
    operational_unit_id = Column(Integer, nullable=False)

    # Relaciones
    comments = relationship("CarrierComment", back_populates="carrier", cascade="all, delete-orphan")
    logs = relationship("CarrierLog", back_populates="carrier", cascade="all, delete-orphan")
    addresses = relationship("CarrierAddress", back_populates="carrier", cascade="all, delete-orphan")


class CarrierCommentModel(Base):
    __tablename__ = "carriers_comments"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    carrier_id = Column(BigInteger, ForeignKey("platform.carriers.id"), nullable=False)
    comments = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=sa.text("now()"))
    created_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True), server_default=sa.text("now()"))
    updated_by = Column(Integer)
    deleted_at = Column(DateTime(timezone=True))
    deleted_by = Column(Integer)

    carrier = relationship("Carrier", back_populates="comments")


class CarrierLogModel(Base):
    __tablename__ = "carriers_logs"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    carrier_id = Column(BigInteger, ForeignKey("platform.carriers.id"), nullable=False)
    changes = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=sa.text('now()'))
    created_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True), server_default=sa.text('now()'))
    updated_by = Column(Integer)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by = Column(Integer, nullable=True)

    carrier = relationship("Carrier", back_populates="logs")


class CarrierAddressModel(Base):
    __tablename__ = "carriers_address"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    carrier_id = Column(BigInteger, ForeignKey("platform.carriers.id"), nullable=False)
    status = Column(String(10))
    code = Column(UUID(as_uuid=True), unique=True, nullable=False, server_default=sa.text('uuid_generate_v4()'))
    place_id = Column(String, nullable=True)
    formatted_address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address_components = Column(JSONB, nullable=False)
    country = Column(String, nullable=False)
    province = Column(String, nullable=False)
    address_type = Column(String, nullable=False)
    description = Column(String, nullable=False)

    carrier = relationship("Carrier", back_populates="addresses")
