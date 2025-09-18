from typing import List, Optional
from pydantic import BaseModel


class Contact(BaseModel):
    emailAddress: str
    description: str


class Routing(BaseModel):
    locationName: str
    locode: str
    countryCode: str
    modeOfTransport: Optional[str] = None
    locationType: Optional[str] = None
    pointUsage: Optional[str] = None
    isSeaPort: bool


class ContainerType(BaseModel):
    label: str


class SectionData(BaseModel):
    name: str
    code: str
    isConsideredForTotal: bool
    currency: str
    container1: Optional[float] = None
    container2: Optional[float] = None
    container3: Optional[float] = None
    additionalNotes: Optional[str] = None


class Section(BaseModel):
    name: str
    label: str
    data: List[SectionData]


class DangerousGoods(BaseModel):
    isHazardous: bool


class HapagQuotation(BaseModel):
    # id: str
    quotationNumber: str
    # validFrom: str
    validTo: str
    expiryDate: str
    # contact: Contact
    # commodityDescription: str
    estimatedTransportDays: int
    routing: List[Routing]
    # exportHaulage: str
    # importHaulage: str
    # containerTypes: List[ContainerType]
    sections: List[Section]
    # includedCharges: List[str]
    # excludedCharges: List[str]
    # notes: List[str]
    # dangerousGoods: DangerousGoods
    start_code: str
    start_name: str
    end_name: str
    end_code: str
