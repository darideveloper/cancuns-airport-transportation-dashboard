from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    LANGS = (
        ("es", "Español"),
        ("en", "Inglés"),
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Título")
    slug = models.SlugField(
        max_length=255, verbose_name="Slug", unique=True, blank=True, null=True
    )
    lang = models.CharField(
        max_length=2, choices=LANGS, default="es", verbose_name="Idioma"
    )
    banner_image_url = models.CharField(
        max_length=255,
        verbose_name="Banner URL",
        help_text="URL de la imagen del banner",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Descripción corta",
    )
    keywords = models.CharField(
        max_length=255,
        verbose_name="Palabras clave",
        help_text="Separadas por comas",
    )
    author = models.CharField(
        max_length=255, verbose_name="Autor", default="Ella Skin & Spa Wellness Team"
    )
    related_post = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Entrada relacionada",
    )
    content = models.TextField(verbose_name="Contenido")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name_plural = "Entradas"
        verbose_name = "Entrada"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        # Override slug if not set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Nombre")
    image = models.ImageField(upload_to="blog/images", verbose_name="Imagen")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )

    class Meta:
        verbose_name_plural = "Imágenes"
        verbose_name = "Imagen"

    def __str__(self):
        return self.name
