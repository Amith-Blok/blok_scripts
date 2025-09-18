from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

from src.utils.convert import camel_camel_to_snake_case


class SectionData(BaseModel):
    model_config = ConfigDict(
        alias_generator=camel_camel_to_snake_case, populate_by_name=True
    )
    name: str
    code: str
    currency: str
    is_considered_for_total: Optional[bool] = None
    additional_notes: Optional[str] = Field(default="")
    d2: Optional[float] = None
    d4: Optional[float] = None
    d5: Optional[float] = None


class Section(BaseModel):
    name: str
    label: str
    data: List[SectionData]


class Route(BaseModel):
    model_config = ConfigDict(
        alias_generator=camel_camel_to_snake_case, populate_by_name=True
    )
    location_name: Optional[str]
    locode: Optional[str]
    country_code: Optional[str]
    mode_of_transport: Optional[str] = None
    location_type: Optional[str] = None
    point_usage: Optional[str] = None
    is_sea_port: Optional[bool]


class LineData(BaseModel):
    model_config = ConfigDict(
        alias_generator=camel_camel_to_snake_case, populate_by_name=True
    )
    line_name: str = Field(default="hapag")
    quotation_number: Optional[str] = None
    estimated_days: int
    valid_to: str
    routing: Optional[List[Route]]
    sections: List[Section]


class Lines(BaseModel):
    model_config = ConfigDict(
        alias_generator=camel_camel_to_snake_case, populate_by_name=True
    )
    start_code: str
    start_name: str
    end_code: str
    end_name: str
    available_lines: List[str]
    lines: List[LineData]
