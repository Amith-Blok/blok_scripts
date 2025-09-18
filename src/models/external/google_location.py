from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from src.utils.convert import camel_camel_to_snake_case


class AddressComponent(BaseModel):
    long_name: str
    short_name: str
    types: List[str]


class Location(BaseModel):
    lat: float
    lng: float


class Viewport(BaseModel):
    northeast: Location
    southwest: Location


class Geometry(BaseModel):
    location: Location
    location_type: str
    viewport: Viewport


class NavigationPointLocation(BaseModel):
    latitude: float
    longitude: float


class NavigationPoint(BaseModel):
    location: NavigationPointLocation


class PlusCode(BaseModel):
    compound_code: Optional[str]
    global_code: str


class GoogleLocationResult(BaseModel):
    address_components: List[AddressComponent]
    formatted_address: str
    geometry: Geometry
    navigation_points: Optional[List[NavigationPoint]] = None
    place_id: str
    plus_code: Optional[PlusCode] = None
    types: List[str]


class GoogleLocationResponse(BaseModel):
    model_config = dict(
        alias_generator=camel_camel_to_snake_case, populate_by_name=True
    )
    results: List[GoogleLocationResult]
    status: str
