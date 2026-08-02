# Cancun Airport Transportation — Dashboard (Blog CRM + Legacy Middleware)

Django dashboard with two roles for the Cancun Airport Transportation ecosystem: a blog/CMS CRM that serves the landing page, and a secure middleware that proxies the legacy Caribbean Transfers booking backend.

## Tech Stack

- **Django 5.2** + **Django REST Framework** — API and models
- **Django Unfold** — modern admin interface
- **django-solo** — singleton models (legacy API token)
- **PostgreSQL** (MySQL and SQLite-for-tests supported)
- **Gunicorn + WhiteNoise** — serving and static files
- **Django Storages (S3-compatible)** — media and static storage
- **requests + selenium** — legacy API proxying and E2E admin tests
- **Docker** — deploy via Coolify and Railway

## Features

- **Blog CRM:** `Post` and `Image` models, Markdown editing with SimpleMDE in the admin, EN/ES localization per post, related posts, SEO fields (keywords, description), read-only DRF API (`/api/posts/`) filtered by `Accept-Language`
- **Legacy middleware:** OAuth token broker with cached, auto-refreshing tokens; five public proxy endpoints (`quote`, `create`, `capture`, `my-booking`, `autocomplete`) that translate fields, inject configuration, generate payment links and validate responses — credentials never exposed to the client
- **Admin:** Unfold-theme admin for posts, images (with copy-link action), users, groups and the legacy token

## Setup

```sh
pip install -r requirements.txt
cp .env.example .env   # configure env
python manage.py migrate
python manage.py runserver
```

---

## Contact

Developed by [Dari Developer](https://darideveloper.com)

- 🌐 [darideveloper.com](https://darideveloper.com)
- 💬 [WhatsApp](https://api.whatsapp.com/send?phone=5214493402622)
- 📂 [View project in portfolio](https://darideveloper.com/portafolio/cancunsairporttransportation)

---

# Cancun Airport Transportation — Dashboard (CRM de Blog + Middleware)

Panel Django con dos funciones para el ecosistema de Cancun Airport Transportation: un CRM de blog que alimenta la landing page y un intermediario seguro que conecta con el sistema de reservas heredado de Caribbean Transfers.

## Tech Stack

- **Django 5.2** + **Django REST Framework** — API y modelos
- **Django Unfold** — interfaz de administración moderna
- **django-solo** — modelos singleton (token de la API heredada)
- **PostgreSQL** (soporta MySQL y SQLite para pruebas)
- **Gunicorn + WhiteNoise** — servidor y archivos estáticos
- **Django Storages (compatible S3)** — almacenamiento de medios y estáticos
- **requests + selenium** — proxy a la API heredada y pruebas E2E del admin
- **Docker** — despliegue en Coolify y Railway

## Features

- **CRM de blog:** modelos `Post` e `Image`, edición Markdown con SimpleMDE en el admin, localización EN/ES por publicación, publicaciones relacionadas, campos SEO (keywords, description), API REST de solo lectura (`/api/posts/`) filtrada por `Accept-Language`
- **Middleware heredado:** broker OAuth con tokens en caché y auto-renovación; cinco endpoints públicos de proxy (`quote`, `create`, `capture`, `my-booking`, `autocomplete`) que traducen campos, inyectan configuración, generan enlaces de pago y validan respuestas — las credenciales nunca se exponen al cliente
- **Admin:** panel con tema Unfold para publicaciones, imágenes (con acción de copiar enlace), usuarios, grupos y el token heredado

## Setup

```sh
pip install -r requirements.txt
cp .env.example .env   # configurar variables
python manage.py migrate
python manage.py runserver
```

---

## Contacto

Desarrollado por [Dari Developer](https://darideveloper.com)

- 🌐 [darideveloper.com](https://darideveloper.com)
- 💬 [WhatsApp](https://api.whatsapp.com/send?phone=5214493402622)
- 📂 [Ver proyecto en el portafolio](https://darideveloper.com/portafolio/cancunsairporttransportation)
