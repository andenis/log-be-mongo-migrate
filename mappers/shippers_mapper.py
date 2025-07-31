from sqlalchemy.orm import Session

from catalog_cache import CatalogCache
from enums.doc_enum import DocStatusEnum
from enums.shipper_enum import ShipperStatusEnum, ShipperParentTypeEnum, ShipperRelationshipTypeEnum
from functions import get_shipper_id_by_old_id, oid_to_catalog_id, bool_or_default, formatear_cuit, \
    normalizar_company_tax_number
from models.shipper_model import ShipperModel


def map_shippers(doc, session: Session):
    cache = CatalogCache()

    doc_id = doc.get("_id", {}).get("$oid", {})
    doc_status = doc.get("shipperStatus", {}).get("status", ShipperStatusEnum.PROSPECT)
    doc_adm_businessName = doc.get("adm", {}).get("businessName", "Error - " + doc_id)
    doc_adm_idNumber = doc.get("adm", {}).get("idNumber", "Error")

    # parent (puede ser None, dict o str)
    parent_oid = doc.get("adm", {}).get("parent")
    if isinstance(parent_oid, dict):
        parent_oid = parent_oid.get("$oid")
    doc_adm_parent_id = get_shipper_id_by_old_id(session, parent_oid)
    doc_adm_parent_type = doc.get("adm", {}).get("parentType", None) #ShipperParentTypeEnum.PARENT if doc_adm_parent_id is not None else ShipperParentTypeEnum.AUTONOMOUS
    if doc_adm_parent_id is not None:
        doc_adm_parent_type = ShipperParentTypeEnum.SON
    else:
        doc_adm_parent_type = doc.get("adm", {}).get("parentType", ShipperParentTypeEnum.AUTONOMOUS)

    doc_adm_comments = doc.get("adm", {}).get("admComments", None)

    # idType
    doc_adm_idType = oid_to_catalog_id(
        doc.get("adm", {}).get("idType"),
        cache,
        default_code="5fd8cc204560a804ab990910",   # OID default
        default_id=3162,                            # ID default en tu catálogo
        field_name="doc_adm_idType"
    )

    # industryType
    doc_adm_industry_type = oid_to_catalog_id(
        doc.get("adm", {}).get("industryType"),
        cache,
        default_code="5fd8cca64560a804ab990923",   # OID default
        default_id=3172,                            # ID default en tu catálogo
        field_name="doc_adm_industry_type"
    )

    # country
    adm_country = oid_to_catalog_id(
        doc.get("adm", {}).get("country"),
        cache,
        default_code="5fd8cc204560a804ab990910",   # OID de AR
        default_id=1,                               # ID de AR en tu tabla destino
        field_name="adm_country"
    )

    doc_sap_card_code = doc.get("sapCardCode")

    doc_adm_reception_office = doc.get("adm", {}).get("receptionOffice")
    doc_adm_reception_office = bool_or_default(doc_adm_reception_office, default=False)

    # relationship_type
    doc_adm_relationship_type = oid_to_catalog_id(
        doc.get("adm", {}).get("relationShipType"),
        cache
    )

    obj = ShipperModel(
        status=get_shipper_status(doc_status),
        doc_status=DocStatusEnum.RED,
        company_name=doc_adm_businessName.upper(),
        company_tax_type=doc_adm_idType,
        company_tax_number= normalizar_company_tax_number(doc_adm_idType, doc_adm_idNumber),
        company_business_type=doc_adm_industry_type,
        company_is_economic_group= (doc_adm_parent_id is not None) or ((doc_adm_parent_type or "").lower() == ShipperParentTypeEnum.PARENT),
        company_parent_type=get_parent_type(doc_adm_parent_type),
        company_parent_shipper_id=doc_adm_parent_id,
        company_relationship_type=get_relationship_type(doc_adm_relationship_type),
        invoice_tax_type_nac=None,
        invoice_tax_number_nac=None,
        invoice_tax_type_int=None,
        invoice_tax_number_int=None,
        reception_office=doc_adm_reception_office,
        company_email="",
        company_phone="",
        company_mobile="",
        country=adm_country,
        is_critical=False,
        admin_accounting_code=None,
        admin_note=doc_adm_comments,
        shipper_contact_id=None,  # TODO: crear proceso aparte para buscar en contactos
        is_deleted=False,
        organization_id=1,  # HUBBING
        operational_unit_id=1,  # HUBBING AR
        old_id=doc_id,
        old_sap_card_code=doc_sap_card_code,
        old_created_at = doc.get("createdAt", {}).get("$date")
    )
    return obj

def get_shipper_status(status):
    mongo_status = status
    match mongo_status:
        case "activo":
            return ShipperStatusEnum.ACTIVE
        case "autorizado":
            return ShipperStatusEnum.ACTIVE
        case "enproceso":
            return ShipperStatusEnum.PROSPECT
        case "prospect":
            return ShipperStatusEnum.PROSPECT
        case "inactivo":
            return ShipperStatusEnum.DISABLED
        case "pendiente":
            return ShipperStatusEnum.PROSPECT
        case "rechazado":
            return ShipperStatusEnum.REJECTED
        case "revision":
            return ShipperStatusEnum.REVIEW

def get_parent_type(type):
    match type:
        case "parent":
            return ShipperParentTypeEnum.PARENT
        case "son":
            return ShipperParentTypeEnum.SON
        case "autonomus":
            return ShipperParentTypeEnum.AUTONOMOUS
        case _:
            return ShipperParentTypeEnum.AUTONOMOUS

def get_relationship_type(type):
    match type:
        case "5fd8cfd24560a804ab990943":
            return ShipperRelationshipTypeEnum.OPERATION
        case "5fd8cfd74560a804ab990944":
            return ShipperRelationshipTypeEnum.BUSINESS_UNIT
        case _:
            return None