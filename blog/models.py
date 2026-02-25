from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    # Django 5 allows using a dictionary for choices directly
    LANGS = {
        "es": "Spanish",
        "en": "English",
    }
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(
        max_length=255, verbose_name="Slug", unique=True, blank=True, null=True
    )
    lang = models.CharField(
        max_length=2,
        choices=LANGS,  # Passing the dictionary directly
        default="es",
        verbose_name="Language",
    )
    banner_image_url = models.CharField(
        max_length=255,
        verbose_name="Banner URL",
        help_text="Banner image URL",
        blank=True,
        null=True,
    )
    description = models.TextField(verbose_name="Short description")
    keywords = models.CharField(
        max_length=255,
        verbose_name="Keywords",
        help_text="Separated by commas",
    )
    author = models.CharField(
        max_length=255, verbose_name="Author", db_default="Ella Skin & Spa Wellness Team"
    )
    related_post = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Related post",
    )
    content = models.TextField(verbose_name="Content")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated at"
    )

    class Meta:
        verbose_name_plural = "Posts"
        verbose_name = "Post"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Override slug if not set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# The Image model remains unchanged as it is already standard.
class Image(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Name")
    image = models.ImageField(upload_to="blog/images", verbose_name="Image")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated at"
    )

    class Meta:
        verbose_name_plural = "Images"
        verbose_name = "Image"

    def __str__(self):
        return self.name
