from django.db import models
from django.conf import settings
from .validators import validate_unit_of_measure
from .utils import number_str_to_float
import pint
User = settings.AUTH_USER_MODEL
# Create your models here.


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,  on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, validators=[
                            validate_unit_of_measure])
    quantity_as_float = models.FloatField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def convert_to_system(self, system='mks'):
        if self.quantity_as_float is None:
            raise ValueError("Quantity as float is not set.")
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg(self.unit)
        return measurement.to_base_units()

    def as_mks(self):
        try:
            measurement = self.convert_to_system(system='mks')
            return measurement
        except Exception as e:
            return str(e)

    def as_imperial(self):
        try:
            measurement = self.convert_to_system(system='imperial')
            return measurement
        except Exception as e:
            return str(e)

    def save(self, *args, **kwargs):
        qty = self.quantity
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)
