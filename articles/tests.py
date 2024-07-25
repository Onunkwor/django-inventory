from django.test import TestCase
from .models import Article
from django.utils.text import slugify
from articles.utils import slugify_instance_title
# Create your tests here.


class ArticleTestCase(TestCase):
    def setUp(self):
        self.number_of_articles = 5
        for i in range(0, self.number_of_articles):
            Article.objects.create(title="Test function",
                                   content="Test function")

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_text_function_slug(self):
        obj = Article.objects.all().order_by('id').first()
        slug = obj.slug
        title = obj.title
        slugified_title = slugify(title)
        self.assertEqual(slug, slugified_title)

    def test_identical_slug(self):
        qs = Article.objects.exclude(slug__iexact='test-function')
        for obj in qs:
            title = obj.title
            slug = obj.slug
            slugified_title = slugify(title)
            self.assertNotEqual(slug, slugified_title)

    def test_slugify_instance_title(self):
        obj = Article.objects.all().last()
        new_slug = []
        for i in range(0, 5):
            instance = slugify_instance_title(obj, save=False)
            new_slug.append(instance.slug)
        unique_slug = list(set(new_slug))
        self.assertEqual(len(unique_slug), len(new_slug))

    def test_slugify_instance_title_redux(self):
        slug_list = Article.objects.all().values_list('slug', flat=True)
        unique_slug_list = list(set(slug_list))
        self.assertEqual(len(unique_slug_list), len(slug_list))

    def test_article_search_manager(self):
        qs = Article.objects.search(query='test')
        self.assertEqual(qs.count(), self.number_of_articles)

    def tearDown(self) -> None:
        Article.objects.all().delete()
        super().tearDown()
