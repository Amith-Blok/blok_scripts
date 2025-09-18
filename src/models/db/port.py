from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class PortLocation(BaseModel):
    type: str = Field(default="Point")
    coordinates: List[float]


class NearestPort(BaseModel):
    port_name: str
    port_code: str


class Port(BaseModel):
    port_name: str
    port_code: str
    port_country: str
    port_region: str
    port_address: str
    port_type: Literal["PORT", "RAIL"]
    nearest_ports: Optional[List[NearestPort]] = None
    place_id: str
    location: PortLocation
    haulage_type: Literal["EXPORT", "IMPORT"] = "EXPORT"
