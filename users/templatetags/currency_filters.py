"""
Custom template filters for currency formatting.

This module provides filters to format decimal/float values as Brazilian Real (R$).
"""
import locale
from decimal import Decimal, InvalidOperation

from django import template


register = template.Library()


def setup_locale():
    """
    Configure locale to pt_BR.UTF-8 for Brazilian currency formatting.

    Falls back to C locale if pt_BR is not available.
    """
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            # Try alternative locale names
            locale.setlocale(locale.LC_ALL, 'pt_BR')
        except locale.Error:
            # Fallback to C locale if pt_BR is not available
            locale.setlocale(locale.LC_ALL, 'C')


@register.filter(name='currency')
def currency(value):
    """
    Format a numeric value as Brazilian Real (R$).

    Args:
        value: Numeric value (int, float, Decimal) or string representation

    Returns:
        str: Formatted currency string (e.g., "R$ 1.234,56")

    Examples:
        {{ 1234.56|currency }}  -> "R$ 1.234,56"
        {{ 0|currency }}        -> "R$ 0,00"
        {{ None|currency }}     -> "R$ 0,00"

    Notes:
        - Handles None values by returning "R$ 0,00"
        - Handles invalid values by returning "R$ 0,00"
        - Uses Brazilian locale for number formatting (thousands: ., decimal: ,)
    """
    # Handle None or empty values
    if value is None or value == '':
        return 'R$ 0,00'

    # Try to convert to Decimal for precise currency calculation
    try:
        if isinstance(value, str):
            # Remove any existing currency symbols and spaces
            value = value.replace('R$', '').replace(' ', '').strip()
            # Replace comma with dot for decimal conversion
            value = value.replace(',', '.')

        decimal_value = Decimal(str(value))
    except (ValueError, InvalidOperation, TypeError):
        # If conversion fails, return zero
        return 'R$ 0,00'

    # Setup locale for Brazilian format
    setup_locale()

    # Format as currency
    try:
        # Format with 2 decimal places and grouping
        formatted = locale.currency(decimal_value, grouping=True, symbol=False)
        return f'R$ {formatted}'
    except (ValueError, locale.Error):
        # Manual formatting fallback
        # Convert to float and format manually
        try:
            float_value = float(decimal_value)
            # Format with Brazilian pattern: thousands separator (.) and decimal comma (,)
            if float_value >= 0:
                integer_part = int(float_value)
                decimal_part = int(round((float_value - integer_part) * 100))
            else:
                integer_part = int(float_value)
                decimal_part = int(round((abs(float_value) - abs(integer_part)) * 100))

            # Format integer part with thousands separator
            integer_str = f'{abs(integer_part):,}'.replace(',', '.')
            if float_value < 0:
                integer_str = f'-{integer_str}'

            return f'R$ {integer_str},{decimal_part:02d}'
        except (ValueError, TypeError):
            return 'R$ 0,00'
