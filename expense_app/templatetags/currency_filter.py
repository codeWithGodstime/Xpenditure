from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='currency')
def currency(value, symbol='$'):
    """
    Formats a number with commas, 2 decimal places, and a currency symbol.
    Example: 1234567.89 -> $1,234,567.89
    """
    try:
        value = Decimal(value)  # Ensure the value is a number
        return f"{symbol}{value:,.2f}"
    except (ValueError, TypeError):
        return value  # Return the original value if there's an error
