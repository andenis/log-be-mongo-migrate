import logging
from datetime import datetime
from sqlalchemy import select
from models.catalog_resource_model import CatalogResourceModel

logger = logging.getLogger(__name__)

class CatalogCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data = []
            cls._instance._last_updated = None
        return cls._instance

    @classmethod
    def load_from_db(cls, session):
        # Síncrono: para migrador o apps sync
        stmt = (
            select(
                CatalogResourceModel.id,
                CatalogResourceModel.code,
                CatalogResourceModel.description,
                CatalogResourceModel.parent_ref
            )
            .where(
                CatalogResourceModel.deleted_at.is_(None),
                CatalogResourceModel.enabled.is_(True)
            )
        )
        result = session.execute(stmt)
        rows = result.fetchall()
        cls()._data = [dict(r._mapping) for r in rows]
        cls()._last_updated = datetime.utcnow()

    @classmethod
    def load_from_db_async(cls, async_session):
        # ASYNC: para microservicios (opcional, si usás SQLAlchemy async)
        # Pero sigue populando el cache sync para consultas inmediatas
        async def _inner():
            async with async_session() as session:
                stmt = (
                    select(
                        CatalogResourceModel.id,
                        CatalogResourceModel.code,
                        CatalogResourceModel.description,
                        CatalogResourceModel.parent_ref
                    )
                    .where(
                        CatalogResourceModel.deleted_at.is_(None),
                        CatalogResourceModel.enabled.is_(True)
                    )
                )
                result = await session.execute(stmt)
                rows = result.fetchall()
                cls()._data = [dict(r._mapping) for r in rows]
                cls()._last_updated = datetime.utcnow()
        return _inner()

    def get_all(self):
        return list(self._data)

    def get_by_code(self, code: str, field_name: str = None):
        for item in self._data:
            if item["code"] == code:
                if field_name:
                    if field_name == "adm_country":
                        return item["parent_ref"]
                    else:
                        return item["id"]

        if field_name:
            logger.warning(f"⚠️ No se encontró ningún recurso con code '{code}' para atributo '{field_name}'")
        else:
            logger.warning(f"⚠️ No se encontró ningún recurso con code '{code}'")
        return None

    def get_last_updated(self):
        return self._last_updated

    @classmethod
    def get_sync(cls):
        # Para compatibilidad, igual que antes
        return cls()._data
