from enum import Enum

# Para un contacto: pending (defecto)
# Se aprueba el contacto: approved
# Se rechaza el contacto: rejected
# Se bloquea el contacto: blocked
class ShipperContactStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    BLOCKED = "blocked"

class ShipperContactSourceEnum(str, Enum):
    COMMERCIAL = "com"
    APP_DRIVER = "app-driver"
    APP_FINDER = "app-finder"
    APP_CARRIER = "app-carrier"
    APP_SHIPPER = "app-shipper"
    APP_CHECK = "app-check"
    WEB = "web"

# Estados en Prospecto y Gestionar
# Pasa como un prospecto: prospect
# Se empieza a trabajar el prospecto: review
# Se rechaza el prospecto: rejected
# Se aprueba para gestionar: active
# Se desactiva en gestionar: disabled
# Se bloquea por algo grave y no se debe usar: blocked
# Se desactiva por documentación vencida: doc_status = "red" y status= "disabled"
class ShipperStatusEnum(str, Enum):
    PROSPECT = "prospect"
    REVIEW = "review"
    REJECTED = "rejected"
    ACTIVE = "active"
    DISABLED = "disabled"
    BLOCKED = "blocked"

class ShipperParentTypeEnum(str, Enum):
    PARENT = "parent"
    SON = "son"
    AUTONOMOUS = "autonomus" # ya estaba mal escrito en el modelo original

class ShipperRelationshipTypeEnum(str, Enum):
    OPERATION = "operation"
    BUSINESS_UNIT = "bussines-unit"