from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import RecipeIngredient, Recipe
# Create your tests here.
User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('raphael', password='abc123')

    def test_user_pw(self):
        checked = self.user_a.check_password('abc123')
        self.assertTrue(checked)


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('raphael', password='abc123')
        self.recipe_a = Recipe.objects.create(
            user=self.user_a, name='Cheese Cake')
        self.recipe_b = Recipe.objects.create(
            user=self.user_a, name='Butter cream')
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            recipe=self.recipe_a, name='Flour', unit='kg', quantity='2')

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_ingredients_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredient_set.all()
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_relation(self):
        user = self.user_a
        qs = RecipeIngredient.objects.filter(recipe__user=user)
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_reverse_relation(self):
        user = self.user_a
        ids = list(user.recipe_set.all().values_list(
            'recipeingredient__id', flat=True))
        qs = RecipeIngredient.objects.filter(id__in=ids)
        self.assertEqual(qs.count(), 1)

    def test_unit_measure_validation_error(self):
        invalid_unit = 'rkfjenvornrouhviv'
        with self.assertRaises(ValidationError):
            ingredients = RecipeIngredient(
                name="New",
                quantity=10,
                recipe=self.recipe_a,
                unit=invalid_unit
            )
            ingredients.full_clean()

    def test_unit_measure_validation(self):
        valid_unit = 'kg'
        ingredients = RecipeIngredient(
            name="New",
            quantity=10,
            recipe=self.recipe_a,
            unit=valid_unit
        )
        ingredients.full_clean()

    def test_quantity_float_error(self):
        test_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe_a, name='Flour', unit='kg', quantity='cake')
        self.assertIsNone(test_ingredient.quantity_as_float)

    def test_quantity_float(self):
        self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float)
