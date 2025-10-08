from pydantic import BaseModel


class DestinationCharges(BaseModel):
    port_code: str
    d2: float
    d4: float
    currency: str