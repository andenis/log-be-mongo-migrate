from enum import Enum

# Para un contacto: pending (defecto)
# Se aprueba el contacto: approved
# Se rechaza el contacto: rejected
# Se bloquea el contacto: blocked
class CarrierContactStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    BLOCKED = "blocked"

class CarrierContactSourceEnum(object):
    COMMERCIAL = "com"
    APP_DRIVER = "app-driver"
    APP_FINDER = "app-finder"
    APP_CARRIER = "app-carrier"
    APP_SHIPPER = "app-shipper"
    APP_CHECK = "app-check"
    WEB = "web"
