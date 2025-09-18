from pydantic import BaseModel
from typing import Optional


class DenormalizeLine(BaseModel):
    # General
    pol: str
    pol_code: str
    pol_hapag_code: str
    pod: str
    pod_code: str
    pod_hapag_code: str

    # HAPAG
    hapag_validity: Optional[str] = None
    hapag_transit_time: Optional[str] = None
    hapag_d2: Optional[float] = None
    hapag_d4: Optional[float] = None

    # MSC
    msc_validity: Optional[str] = None
    msc_transit_time: Optional[str] = None
    msc_d2: Optional[float] = None
    msc_d4: Optional[float] = None

    # ONE
    one_validity: Optional[str] = None
    one_transit_time: Optional[str] = None
    one_d2: Optional[float] = None
    one_d4: Optional[float] = None

    # MSC
    msc_validity: Optional[str] = None
    msc_transit_time: Optional[str] = None
    msc_d2: Optional[float] = None
    msc_d4: Optional[float] = None

    # HMM
    hmm_validity: Optional[str] = None
    hmm_transit_time: Optional[str] = None
    hmm_d2: Optional[float] = None
    hmm_d4: Optional[float] = None

    # CMA
    cma_validity: Optional[str] = None
    cma_transit_time: Optional[str] = None
    cma_d2: Optional[float] = None
    cma_d4: Optional[float] = None

    # WANHAI
    wanhai_validity: Optional[str] = None
    wanhai_transit_time: Optional[str] = None
    wanhai_d2: Optional[float] = None
    wanhai_d4: Optional[float] = None

    # SEA LEAD
    sealead_validity: Optional[str] = None
    sealead_transit_time: Optional[str] = None
    sealead_d2: Optional[float] = None
    sealead_d4: Optional[float] = None


class DenormalizeLine(BaseModel):
    pol_code: str
    pol_name:str
    pod_code: str
    pod_name:str
    line_name: str
    transit_time: int
    validity: str
    d2: float
    d4: float
