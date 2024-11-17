from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import test, status
from rest_framework.test import APIClient
from django.urls import reverse
from core.models import Ingredient, Recipe, Tag
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')

# recipe/recipes/<id>


def get_detail_url(recipe_id):
    print(recipe_id)
    return reverse('recipe:recipe-detail', args=[recipe_id])


def generate_sample_tag(user, name='Main tag'):
    return Tag.objects.create(user=user, name=name)


def generate_sample_ingredient(user, name='Main tag', amount=10):
    return Ingredient.objects.create(user=user, name=name, amount=amount)


def generate_sample_recipe(user, **params):
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 999,
        'cost': 5.00
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@sample.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_get_recipes(self):
        generate_sample_recipe(user=self.user)
        generate_sample_recipe(user=self.user)
        generate_sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-title')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        recipe = generate_sample_recipe(user=self.user)
        recipe.tags.add(generate_sample_tag(user=self.user))
        recipe.ingredients.add(generate_sample_ingredient(user=self.user))

        detail_url = get_detail_url(recipe_id=recipe.id)
        res = self.client.get(detail_url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update_recipe(self):
        recipe = generate_sample_recipe(user=self.user)
        recipe.tags.add(generate_sample_tag(user=self.user))
        recipe.ingredients.add(generate_sample_ingredient(user=self.user))

        new_tag = generate_sample_tag(user=self.user, name='deshi')
        payload = {'title': 'Morog Polao', 'tags': [new_tag.id]}

        detail_url = get_detail_url(recipe_id=recipe.id)
        self.client.patch(detail_url, payload)

        recipe.refresh_from_db()

        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        recipe = generate_sample_recipe(user=self.user)
        recipe.tags.add(generate_sample_tag(user=self.user))
        recipe.ingredients.add(generate_sample_ingredient(user=self.user))

        payload = {'title': 'Burger', 'time_minutes': 15, 'cost': 225}

        detail_url = get_detail_url(recipe_id=recipe.id)
        self.client.put(detail_url, payload)

        recipe.refresh_from_db()

        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.cost, payload['cost'])
