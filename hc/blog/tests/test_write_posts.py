from hc.test import BaseTestCase
from django.core.urlresolvers import reverse
from hc.blog.models import Post, Category, Comment


class WritePostsTestCase(BaseTestCase):
    def setUp(self):
        super(WritePostsTestCase, self).setUp()
        self.category = Category(title="test category", owner=self.alice)
        self.category.save()
        self.post = Post(title="test post", slug="test-post", body="test content",
                         author=self.alice, status="draft", category=self.category)
        self.post.save()
        self.client.login(username="alice@example.org", password="password")
        self.form = {
            "status": "draft",
            "category": self.category.id,
            "title": "my blog post",
            "body": "my blog post content",
            "publish": "08/08/2018 12:00 AM"
        }

    def test_it_renders_posts(self):
        res = self.client.get(reverse("hc-my-posts"))
        self.assertContains(res, self.post.title)

    def test_it_creates_post(self):
        res = self.client.post(reverse("hc-add-post"), self.form)
        self.assertRedirects(res, reverse("hc-my-posts"))

    def test_it_edits_post(self):
        res = self.client.post(
            reverse("hc-edit-post", kwargs={"post_id": self.post.id}), self.form)
        self.assertRedirects(res, reverse("hc-my-posts"))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, self.form.get("title"))

    def test_it_removes_post(self):
        res = self.client.delete(
            reverse("hc-remove-post", kwargs={"post_id": self.post.id}))
        self.assertContains(res, "message")
        self.assertEqual(res.status_code, 200)

    def test_it_creates_category(self):
        res = self.client.post(reverse("hc-add-category"),
                               {"title": 'new-category'})
        self.assertContains(res, "message")
        self.assertEqual(res.status_code, 200)

    def test_does_not_edit_post_with_wrong_date(self):
        # set wrong date
        self.form['publish'] = "Wrong date"
        res = self.client.post(reverse("hc-add-post"), self.form)
        self.assertContains(res, "<li>Enter valid date and time</li>")

    def test_does_not_edit_post_with_wrong_date(self):
        self.form['publish'] = "Wrong date"
        res = self.client.post(
            reverse("hc-edit-post", kwargs={"post_id": self.post.id}), self.form)
        self.assertContains(res, "<li>Enter valid date and time</li>")
