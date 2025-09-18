from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class AirportLocation(BaseModel):
    type: str = Field(default="Point")
    coordinates: List[float]


class NearestAirport(BaseModel):
    port_name: str
    port_code: str


class Airport(BaseModel):
    port_name: str
    port_code: str
    port_country: str
    port_region: str
    port_address: str
    port_type: Literal["AIRPORT"]
    port_country_name: str
    place_id: str
    location: AirportLocation