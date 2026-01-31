from django.test import TestCase

from blog import models as blog_models

from utils.media import get_test_image


class TestPostsModelBase(TestCase):
    """Test blog models"""

    def create_post(
        self,
        title: str = "Post test",
        lang: str = "es",
        description: str = "Test description",
        keywords: str = "test, keywords",
        author: str = "Ella Skin & Spa Wellness Team",
        content: str = "#Test \n**conten**t",
    ) -> blog_models.Post:
        """Create a post object"""

        return blog_models.Post.objects.create(
            title=title,
            lang=lang,
            description=description,
            keywords=keywords,
            author=author,
            content=content,
        )

    def create_image(
        self,
        post: blog_models.Post = None,
        name: str = "Image test",
        image_name: str = "test.webp",
    ) -> blog_models.Image:
        """Create a image object"""

        if not post:
            post = self.create_post()

        image_file = get_test_image(image_name)

        return blog_models.Image.objects.create(
            name=name,
            image=image_file,
        )
