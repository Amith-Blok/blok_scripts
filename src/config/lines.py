US_SEAFRIEGHT_MAPPER = {
    # General
    "pol": "pol",
    "pod": "pod",
    # Hapag
    "validity": "hapag_validity",
    "transit time": "hapag_transit_time",
    "hapag": "hapag_d2",
    "hapag.1": "hapag_d4",
    # CMA
    "validity.1": "cma_validity",
    "transit time.1": "cma_transit_time",
    "cma": "cma_d2",
    "cma.1": "cma_d4",
    # ONE
    "validity.2": "one_validity",
    "transit time.2": "one_transit_time",
    "one": "one_d2",
    "one.1": "one_d4",
    # MSC
    "validity.3": "msc_validity",
    "transit time.3": "msc_transit_time",
    "msc": "msc_d2",
    "msc.1": "msc_d4",
    # HMM
    "validity.4": "hmm_validity",
    "transit time.4": "hmm_transit_time",
    "hmm": "hmm_d2",
    "hmm.1": "hmm_d4",
    # Sea Lead
    "validity.5": "sealead_validity",
    "transit time.5": "sealead_transit_time",
    "sea lead": "sealead_d2",
    "sea lead.1": "sealead_d4",
    # Cosco
    "validity.6": "cosco_validity",
    "transit time.6": "cosco_transit_time",
    "cosco": "cosco_d2",
    "cosco.1": "cosco_d4",
}

EU_SEAFRIEGHT_MAPPER = {
    # General
    "pol": "pol",
    "pod": "pod",
    # Hapag
    "validity": "hapag_validity",
    "transit time": "hapag_transit_time",
    "hapag": "hapag_d2",
    "hapag.1": "hapag_d4",
    # MSC
    "validity.1": "msc_validity",
    "transit time.1": "msc_transit_time",
    "msc": "msc_d2",
    "msc.1": "msc_d4",
    # ONE
    "validity.2": "one_validity",
    "transit time.2": "one_transit_time",
    "one": "one_d2",
    "one.1": "one_d4",
    # HMM
    "validity.3": "hmm_validity",
    "transit time.3": "hmm_transit_time",
    "hmm": "hmm_d2",
    "hmm.1": "hmm_d4",
    # CMA
    "validity.4": "cma_validity",
    "transit time.4": "cma_transit_time",
    "cma": "cma_d2",
    "cma.1": "cma_d4",
    # Wanhai
    # "validity.5": "wanhai_validity",
    # "transit time.5": "wanhai_transit_time",
    # "wanhai": "wanhai_d2",
    # "wanhai.1": "wanhai_d4",
}
FE_ME_AF_CN_SEAFIEGHT_MAPPER = {
    # General
    "pol": "pol",
    "pod": "pod",
    # OOCL
    "validity": "oocl_validity",
    "transit time": "oocl_transit_time",
    "oocl": "oocl_d2",
    "oocl.1": "oocl_d4",
}
OC_SEAFIEGHT_MAPPER = {
    # General
    "pol": "pol",
    "pod": "pod",
    # OOCL
    "validity": "oocl_validity",
    "transit time": "oocl_transit_time",
    "oocl": "oocl_d2",
    "oocl.1": "oocl_d4",
    # Hapag
    "validity.1": "hapag_validity",
    "transit time.1": "hapag_transit_time",
    "hapag": "hapag_d2",
    "hapag.1": "hapag_d4",
    # MSC
    "validity.2": "msc_validity",
    "transit time.2": "msc_transit_time",
    "msc": "msc_d2",
    "msc.1": "msc_d4",
}
ALL_LINES = [
    "msc",
    "hapag",
    "one",
    "cma",
    "wanhai",
    "hmm",
    "oocl",
    "sea_lead",
    "cosco",
    "sealead",
]
LINE_SCAC_MAPPING = {
    "msc": "MSCU",
    "hapag": "HLCU",
    "hmm": "HDMU",
    "wanhai": "WHLC",
    "cma": "CMDU",
    "one": "ONEY",
    "sealead": "SCLD",
}
