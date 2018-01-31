from decimal import Decimal, InvalidOperation
import re


def coerce_to_decimal(value):
    if isinstance(value, str):
        value = re.sub('[^0-9\.]+', '', value)
    try:
        return Decimal(value)
    except (TypeError, ValueError, InvalidOperation):
        return None
