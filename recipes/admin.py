from django.contrib.auth import get_user_model
from django.contrib import admin
from .models import RecipeIngredient, Recipe
# Register your models here.

# User = get_user_model()

# admin.site.unregister(User)


# class RecipeInline(admin.StackedInline):
# model = Recipe
# fields = ['name', 'quantity', 'unit', 'directions']
# extra = 0


# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username']
#     inlines = [RecipeInline]


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    # fields = ['name', 'quantity', 'unit', 'directions']
    extra = 0
    readonly_fields = ['quantity_as_float', 'as_mks', 'as_imperial']


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['name', 'user']
    readonly_fields = ['timestamp', 'updated']
    raw_id_fields = ['user']


admin.site.register(Recipe, RecipeAdmin)

admin.site.register(RecipeIngredient)

# admin.site.register(User, UserAdmin)
