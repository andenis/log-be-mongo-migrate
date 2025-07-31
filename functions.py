from sqlalchemy.orm import Session

from models.shipper_model import ShipperModel


def print_getters_for_mapping(docs):
    """
    Imprime el nombre de la tabla en mayúsculas y líneas con
    solo el acceso seguro tipo doc.get("a", {}).get("b", {}) para todos los atributos.
    """
    ignore_keys = {'__v'}

    paths = set()

    def collect_paths(doc, prefix=[]):
        for k, v in doc.items():
            if k in ignore_keys:
                continue
            current_path = prefix + [k]
            paths.add(tuple(current_path))
            if isinstance(v, dict):
                collect_paths(v, current_path)
            elif isinstance(v, list) and v and isinstance(v[0], dict):
                collect_paths(v[0], current_path)

    for doc in docs:
        collect_paths(doc)

    for path in sorted(paths):
        access = "doc"
        for k in path:
            access += f'.get("{k}", {{}})'
        print(access)


def get_shipper_id_by_old_id(session: Session, old_id_value):
    result = session.query(ShipperModel.id).filter(ShipperModel.old_id == old_id_value).first()
    if result:
        return result[0]  # Devuelve el id
    return None


def bool_or_default(value, default=False):
    # Devuelve el booleano si no es None, sino el default
    return bool(value) if value is not None else default


def oid_to_catalog_id(oid_raw, cache, default_code=None, default_id=None, field_name=None):
    """
    Dado un dict con '$oid', un string, o None, busca el id en el catálogo por código.
    Si no existe, devuelve default_id si lo pasás, si no devuelve None.
    Loggea el campo consultado si no se encuentra.
    """
    if isinstance(oid_raw, dict):
        code = oid_raw.get("$oid")
    else:
        code = oid_raw

    if not code:
        code = default_code

    catalog_id = cache.get_by_code(code, field_name=field_name) if code else None
    return catalog_id if catalog_id is not None else default_id

def formatear_cuit(cuit: str) -> str:
    # Argentina
    if cuit and len(cuit) == 11 and cuit.isdigit():
        return f"{cuit[:2]}-{cuit[2:10]}-{cuit[10]}"
    return cuit

def formatear_ruc_paraguay(ruc: str) -> str:
    # Paraguay
    if ruc and len(ruc) in (8, 9) and ruc.isdigit():
        return f"{ruc[:-1]}-{ruc[-1]}"
    return ruc

def formatear_rut_uruguay(rut: str) -> str:
    # Uruguay: usualmente 12 dígitos (sin máscara), o con guión después del noveno.
    if rut and len(rut) == 12 and rut.isdigit():
        return f"{rut[:9]}-{rut[9:]}"
    elif rut and len(rut) == 11 and rut.isdigit():
        return f"{rut[:8]}-{rut[8:]}"
    return rut

def formatear_nit_bolivia(nit: str) -> str:
    # Bolivia: no hay máscara fija, puede ir como viene.
    return nit

def formatear_rut_chile(rut: str) -> str:
    # Chile: 8 o 9 dígitos, último es dígito verificador (puede ser K)
    if rut and len(rut) in (8, 9):
        # Si termina en K o k
        if rut[-1].upper() == 'K' or rut[-1].isdigit():
            return f"{rut[:-1]}-{rut[-1].upper()}"
    return rut

def formatear_cnpj_brasil(cnpj: str) -> str:
    # Brasil: XX.XXX.XXX/XXXX-XX
    if cnpj and len(cnpj) == 14 and cnpj.isdigit():
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj

def formatear_rif_venezuela(rif: str) -> str:
    # Venezuela: J-XXXXXXXX-X (puede iniciar con V, E, G, J, P, C)
    import re
    match = re.match(r"^([JVGEPCAjvgepc])?(\d{8})[\-]?(\d)$", rif)
    if match:
        letra = match.group(1).upper() if match.group(1) else 'J'
        nums = match.group(2)
        verif = match.group(3)
        return f"{letra}-{nums}-{verif}"
    return rif

def formatear_nit_colombia(nit: str) -> str:
    # Colombia NIT: 9-10 dígitos + guión + dígito verificador
    import re
    nit_digits = re.sub(r'\D', '', nit)
    if len(nit_digits) in (9, 10) and nit and ('-' not in nit):
        # El último dígito es el verificador
        return f"{nit_digits[:-1]}-{nit_digits[-1]}"
    return nit

def formatear_ruc_ecuador(ruc: str) -> str:
    # Ecuador: 13 dígitos, sin máscara específica
    ruc_digits = ''.join(filter(str.isdigit, str(ruc)))
    if len(ruc_digits) == 13:
        return ruc_digits
    return ruc

def formatear_ruc_peru(ruc: str) -> str:
    # Perú: 11 dígitos, sin máscara específica
    ruc_digits = ''.join(filter(str.isdigit, str(ruc)))
    if len(ruc_digits) == 11:
        return ruc_digits
    return ruc

def normalizar_company_tax_number(tax_type: int, number: str) -> str:
    if not number:
        return number

    code = str(tax_type)
    if code == "3162":       # Argentina CUIT
        return formatear_cuit(number)
    elif code == "3171":     # Paraguay RUC
        return formatear_ruc_paraguay(number)
    elif code == "3164":     # Uruguay RUT
        return formatear_rut_uruguay(number)
    elif code == "3170":     # Bolivia NIT
        return formatear_nit_bolivia(number)
    elif code == "3165":     # Chile RUT
        return formatear_rut_chile(number)
    elif code == "3163":     # Brasil CNPJ
        return formatear_cnpj_brasil(number)
    elif code == "3168":     # Venezuela RIF
        return formatear_rif_venezuela(number)
    elif code == "3166":     # Colombia NIT
        return formatear_nit_colombia(number)
    elif code == "3167":     # Ecuador RUC
        return formatear_ruc_ecuador(number)
    elif code == "3169":     # Perú RUC
        return formatear_ruc_peru(number)
    else:
        return number


def upsert_by_field(session, obj, unique_field='old_id'):
    """
    Hace upsert: actualiza si ya existe (por unique_field), inserta si no.
    - session: SQLAlchemy session
    - obj: instancia del modelo a insertar/actualizar
    - unique_field: nombre del campo único (default: 'old_id')
    """
    # Obtener valor único
    unique_value = getattr(obj, unique_field)
    ModelClass = obj.__class__
    existing = session.query(ModelClass).filter(getattr(ModelClass, unique_field) == unique_value).first()
    if existing:
        # Actualiza todos los campos menos id y _sa_instance_state
        for attr, value in obj.__dict__.items():
            if attr not in ["_sa_instance_state", "id"]:
                setattr(existing, attr, value)
        return 'update'
    else:
        session.add(obj)
        return 'insert'
