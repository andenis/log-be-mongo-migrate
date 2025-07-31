from sqlalchemy import (
    Column, BigInteger, Integer, String, Boolean, Text, DateTime, ForeignKey, Float, CHAR
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

Base = declarative_base()

class ShipperModel(Base):
    __tablename__ = "shippers"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True)
    code = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    status = Column(String(20))
    doc_status = Column(String(20))
    company_name = Column(Text, nullable=False)
    company_tax_type = Column(Integer, nullable=False)
    company_tax_number = Column(String(30), nullable=False)
    company_business_type = Column(Integer, nullable=False)
    company_is_economic_group = Column(Boolean, nullable=False, server_default="false")
    company_parent_type = Column(String(10), nullable=True)
    company_parent_shipper_id = Column(BigInteger, nullable=True)
    company_relationship_type = Column(String(30), nullable=True)
    invoice_tax_type_nac = Column(Integer, nullable=True)
    invoice_tax_number_nac = Column(String(30), nullable=True)
    invoice_tax_type_int = Column(Integer, nullable=True)
    invoice_tax_number_int = Column(String(30), nullable=True)
    reception_office = Column(Boolean, nullable=False, server_default="false")
    company_email = Column(String(200), nullable=True)
    company_phone = Column(String(50))
    company_mobile = Column(String(50), nullable=True)
    country = Column(CHAR(2), nullable=False)
    is_critical = Column(Boolean, nullable=False, server_default="false")
    admin_accounting_code = Column(String(50))
    admin_note = Column(Text, nullable=True)
    shipper_contact_id = Column(Integer, nullable=True)
    old_id = Column(String(50), unique=True)
    old_sap_card_code = Column(String(100))
    old_created_at = Column(DateTime(timezone=True))
    old_updated_at = Column(DateTime(timezone=True))
    is_deleted = Column(Boolean, nullable=False, server_default="false")
    organization_id = Column(Integer, nullable=False)
    operational_unit_id = Column(Integer, nullable=False)

    # Relaciones
    comments = relationship("ShipperCommentModel", back_populates="shipper")
    logs = relationship("ShipperLogModel", back_populates="shipper")
    addresses = relationship("ShipperAddressModel", back_populates="shipper")
    # contacts = relationship("ShipperContactModel", back_populates="shipper")  # Si tienes este modelo

class ShipperCommentModel(Base):
    __tablename__ = "shippers_comments"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True)
    shipper_id = Column(BigInteger, ForeignKey("platform.shippers.id"), nullable=False)
    comments = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True))
    created_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True))
    updated_by = Column(Integer)
    deleted_at = Column(DateTime(timezone=True))
    deleted_by = Column(Integer)

    shipper = relationship("ShipperModel", back_populates="comments")

class ShipperLogModel(Base):
    __tablename__ = "shippers_logs"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True)
    shipper_id = Column(BigInteger, ForeignKey("platform.shippers.id"), nullable=False)
    changes = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True))
    created_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True))
    updated_by = Column(Integer)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by = Column(Integer, nullable=True)

    shipper = relationship("ShipperModel", back_populates="logs")

class ShipperAddressModel(Base):
    __tablename__ = "shippers_address"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True)
    shipper_id = Column(BigInteger, ForeignKey("platform.shippers.id"), nullable=False)
    status = Column(String(10))
    code = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    place_id = Column(String, nullable=True)
    formatted_address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address_components = Column(JSONB, nullable=False)
    country = Column(String, nullable=False)
    province = Column(String, nullable=False)
    address_type = Column(String, nullable=False)
    description = Column(String, nullable=False)

    shipper = relationship("ShipperModel", back_populates="addresses")
