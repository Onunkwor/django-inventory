from django.core.exceptions import ValidationError
import pint
from pint.errors import UndefinedUnitError

# valid_unit_measurements = ['pounds', 'lbs', 'oz', 'grams']


def validate_unit_of_measure(value):
    ureg = pint.UnitRegistry()
    try:
        ureg(value)
    except UndefinedUnitError as e:
        raise ValidationError(f'"{e}" is not a valid unit of measurement')
    except:
        raise ValidationError(f'"{value}" is invalid. Unknown error')