from sqlalchemy.orm import Session

from catalog_cache import CatalogCache
from models.carrier_model import CarrierModel


def map_carriers(docsession: Session):
    cache = CatalogCache()

    old_id = doc.get("old_id") or str(doc.get("_id"))
    return CarrierModel(
        code=doc.get("code"),
        name=doc.get("name"),
        contact=doc.get("contact"),
        old_id=old_id
    )