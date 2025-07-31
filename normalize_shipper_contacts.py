import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# --- Funciones de formateo ---
def formatear_cuit(cuit: str) -> str:
    if cuit and len(cuit) == 11 and cuit.isdigit():
        return f"{cuit[:2]}-{cuit[2:10]}-{cuit[10]}"
    return cuit

def formatear_ruc_paraguay(ruc: str) -> str:
    if ruc and len(ruc) in (8, 9) and ruc.isdigit():
        return f"{ruc[:-1]}-{ruc[-1]}"
    return ruc

def formatear_rut_uruguay(rut: str) -> str:
    if rut and len(rut) == 12 and rut.isdigit():
        return f"{rut[:9]}-{rut[9:]}"
    elif rut and len(rut) == 11 and rut.isdigit():
        return f"{rut[:8]}-{rut[8:]}"
    return rut

def formatear_nit_bolivia(nit: str) -> str:
    return nit

def formatear_rut_chile(rut: str) -> str:
    if rut and len(rut) in (8, 9):
        if rut[-1].upper() == 'K' or rut[-1].isdigit():
            return f"{rut[:-1]}-{rut[-1].upper()}"
    return rut

def formatear_cnpj_brasil(cnpj: str) -> str:
    if cnpj and len(cnpj) == 14 and cnpj.isdigit():
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj

def formatear_rif_venezuela(rif: str) -> str:
    import re
    match = re.match(r"^([JVGEPCAjvgepc])?(\d{8})[\-]?(\d)$", rif)
    if match:
        letra = match.group(1).upper() if match.group(1) else 'J'
        nums = match.group(2)
        verif = match.group(3)
        return f"{letra}-{nums}-{verif}"
    return rif

def formatear_nit_colombia(nit: str) -> str:
    import re
    nit_digits = re.sub(r'\D', '', nit)
    if len(nit_digits) in (9, 10) and nit and ('-' not in nit):
        return f"{nit_digits[:-1]}-{nit_digits[-1]}"
    return nit

def formatear_ruc_ecuador(ruc: str) -> str:
    ruc_digits = ''.join(filter(str.isdigit, str(ruc)))
    if len(ruc_digits) == 13:
        return ruc_digits
    return ruc

def formatear_ruc_peru(ruc: str) -> str:
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

# --- PROCESO DE NORMALIZACIÓN ---
def main():
    # Carga la config con la conexión a Postgres
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)
    POSTGRES_URL = config["postgres"]["url"]

    engine = create_engine(POSTGRES_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Lee todos los shippers_contacts
    contacts = session.execute(
        text("SELECT id, company_tax_type, company_tax_number, company_name FROM platform.shippers_contacts")
    ).fetchall()

    updates = 0
    for row in contacts:
        cid = row[0]
        tax_type = row[1]
        tax_number = row[2]
        company_name = row[3] or ""

        if not tax_number and not company_name:
            continue

        normalized = normalizar_company_tax_number(tax_type, tax_number) if tax_number else None
        normalized_name = company_name.upper()

        to_update = {}
        if tax_number and normalized != tax_number:
            to_update["company_tax_number"] = normalized
        if company_name and company_name != normalized_name:
            to_update["company_name"] = normalized_name

        if to_update:
            set_clause = ", ".join([f"{k} = :{k}" for k in to_update.keys()])
            params = {**to_update, "cid": cid}
            session.execute(
                text(f"UPDATE platform.shippers_contacts SET {set_clause} WHERE id = :cid"),
                params
            )
            print(f"UPDATE: id={cid} ", ", ".join([f"{k}: '{row[i+2]}' → '{v}'" for i, (k, v) in enumerate(to_update.items())]))
            updates += 1

    session.commit()
    print(f"Total de shippers_contacts actualizados: {updates}")

    session.close()

if __name__ == "__main__":
    main()
