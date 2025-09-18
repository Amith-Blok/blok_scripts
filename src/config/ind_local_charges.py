BL_FEES = 5100
MANIFEST_DOC_FEES = 3750
EXPORT_FEES_20STD = 1600
EXPORT_FEES_40STD = 2118

INDIA_EXPORT_LOCAL_CHARGES = [
        {
            "name": "Bill of Lading Fee",
            "label": "Document Charge BL Fee",
            "container1": BL_FEES,
            "container2": BL_FEES,
            "container3": BL_FEES,
            "currency": "INR",
            "code": "BLF",
        },
        {
            "label": "Security Manifest Document",
            "container1": MANIFEST_DOC_FEES,
            "container2": MANIFEST_DOC_FEES,
            "container3": MANIFEST_DOC_FEES,
            "currency": "INR",
            "code": "MDF",
        },
        {
            "label": "Export Fees",
            "container1": EXPORT_FEES_20STD,
            "container2": EXPORT_FEES_40STD,
            "container3": EXPORT_FEES_40STD,
            "currency": "INR",
            "code": "ESF",
        },
]
