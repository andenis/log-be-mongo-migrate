from enum import Enum

# Para el control documental: red (defecto)
# Todos los docuentos obligatorios cargados y sin vencer: green
# Todos los docuentos obligatorios cargados y algunos por vencer: yellow
# Todos o algunos docuentos obligatorios faltan cargar y/o vencidos: red
class DocStatusEnum(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"