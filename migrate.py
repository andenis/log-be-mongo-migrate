import json
import zipfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_cache import CatalogCache
from functions import print_getters_for_mapping, upsert_by_field

# Mappers deben estar en el mismo directorio que migrate.py
from mappers.shippers_mapper import map_shippers
from mappers.carriers_mapper import map_carriers
from models.catalog_resource_model import CatalogResourceModel

def main():
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)

    POSTGRES_URL = config["postgres"]["url"]
    engine = create_engine(POSTGRES_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # CARGA EL CATÁLOGO
    CatalogCache.load_from_db(session)
    print(f"Catálogo cargado en memoria: {len(CatalogCache.get_sync())} recursos.")

    for migration in config["migrations"]:
        # Solo ejecutar si enabled = True
        if not migration.get("enabled", False):
            print(f"Migration {migration.get('table', '?')} deshabilitada. Skipping.")
            continue

        mongo_file = migration["file"]
        table = migration["table"]
        func_name = migration.get("map_func")

        # Descomprimir si es ZIP
        if mongo_file.endswith(".zip"):
            with zipfile.ZipFile("files/" + mongo_file, 'r') as zip_ref:
                zip_ref.extractall(".")
                for filename in zip_ref.namelist():
                    if filename.endswith(".json"):
                        json_file = filename
                        break
        else:
            json_file = mongo_file

        # Leer JSON
        with open("files/" + json_file, encoding="utf-8") as f:
            try:
                docs = json.load(f)
                if table == "shippers":
                    docs = sorted(
                        docs,
                        key=lambda doc: (doc.get("adm", {}).get("parentType") or "")
                    )
            except Exception:
                docs = [json.loads(line) for line in f]

        if not docs:
            print(f"El archivo {mongo_file} no tiene datos. Skipping.")
            continue

        # Para imprimir el árbol de atributos del documento
        print(f"\nMigrando {len(docs)} registros a la tabla '{table}'...")
        print_getters_for_mapping(docs)

        # Buscar función de mapeo
        mapper = globals().get(func_name)
        if not callable(mapper):
            print(f"Función de mapeo '{func_name}' no encontrada. Skipping.")
            continue

        # Migrar
        count_insert = 0
        count_update = 0
        for doc in docs:
            obj = mapper(doc, session)
            result = upsert_by_field(session, obj, unique_field="old_id")
            if result == "insert":
                count_insert += 1
            else:
                count_update += 1
        session.commit()
        print(f"Insertados: {count_insert}, Actualizados: {count_update}")

    session.close()
    print("Todas las migraciones finalizadas.")

if __name__ == "__main__":
    main()
