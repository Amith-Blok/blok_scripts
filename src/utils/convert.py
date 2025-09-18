import unicodedata
import re


def remove_diacritics(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def camel_camel_to_snake_case(string: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()

def string_to_snake_case(string: str) -> str:
    return re.sub(r"\s+", "_", string).lower()