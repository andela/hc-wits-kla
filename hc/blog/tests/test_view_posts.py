from hc.test import BaseTestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from hc.blog.models import Post, Category, Comment


class ViewPostsTestCase(BaseTestCase):
    def setUp(self):
        super(ViewPostsTestCase, self).setUp()
        self.category = Category(title="test-category", owner=self.alice)
        self.category.save()
        self.post = Post(title="test post", slug="test-post", body="test content",
                         author=self.alice, status="published",
                         category=self.category, publish=timezone.now())
        self.post.save()
        self.client.login(username="alice@example.org", password="password")

    def test_it_renders_published_posts(self):
        res = self.client.get(reverse("hc-blog"))
        self.assertContains(res, self.post.title)

    def test_renders_categorised_posts(self):
        url = "{0}?category={1}".format(
            reverse("hc-blog"), self.category.title)
        res = self.client.get(url)
        self.assertContains(res, self.category.title)

    def test_view_post(self):
        # get url for post to view
        url = self.post.get_view_absolute_url()
        res = self.client.get(url)
        self.assertContains(res, self.post.title)

    def test_comment_on_post(self):
        # get url for post to comment on
        url = self.post.get_view_absolute_url()
        form = {
            "name": "solo",
            "email": "solo@example.org",
            "body": "my comment content",
        }
        res = self.client.post(url, form)
        self.assertContains(res, form.get('body'))
