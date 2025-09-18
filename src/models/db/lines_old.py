from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

from src.utils.convert import camel_camel_to_snake_case


class OldSectionData(BaseModel):
    name: str
    code: str
    currency: str
    is_considered_for_total: Optional[bool] = Field(
        default=True, alias="isConsideredForTotal"
    )
    additional_notes: Optional[str] = Field(default=None, alias="additionalNotes")
    d2: Optional[float] = Field(default=None, alias="container1")
    d4: Optional[float] = Field(default=None, alias="container2")
    d5: Optional[float] = Field(default=None, alias="container3")


class OldSection(BaseModel):
    name: str
    label: str
    data: List[OldSectionData]


class OldRoute(BaseModel):
    location_name: Optional[str] = Field(alias="locationName")
    locode: Optional[str]
    country_code: Optional[str] = Field(alias="countryCode")
    mode_of_transport: Optional[str] = Field(default=None, alias="modeOfTransport")
    location_type: Optional[str] = Field(default=None, alias="locationType")
    point_usage: Optional[str] = Field(default=None, alias="pointUsage")
    is_sea_port: Optional[bool] = Field(default=None, alias="isSeaPort")


class OldLineData(BaseModel):
    model_config = ConfigDict(
        alias_generator=camel_camel_to_snake_case,
        populate_by_name=True,
        from_attributes=True,
    )
    start_code: str
    start_name: str
    end_code: str
    end_name: str
    line_name: str = Field(default="hapag")
    quotation_number: Optional[str] = None
    estimated_days: int
    valid_to: str
    routing: List[OldRoute]
    charges: List[OldSection]
