# Django Unfold Integration Guide

This document describes how `django-unfold` is integrated into this project to provide a modern, responsive, and customizable Django Admin interface.

## 1. Dependencies

Add the following package to your `requirements.txt`:

```text
django-unfold==0.77.1
```

## 2. Configuration in `settings.py`

### 2.1 Installed Apps

Ensure `unfold` and its optional components are placed **before** `django.contrib.admin`:

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    # ... other apps
    "django.contrib.admin",
    # ...
]
```

### 2.2 Templates Configuration

Add the project templates directory to allow overriding admin templates (e.g., `admin/base.html`):

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "project", "templates")],
        "APP_DIRS": True,
        # ...
    },
]
```

### 2.3 Global Settings (Optional but Recommended)

For consistent date/time display across the admin:

```python
DATE_FORMAT = "d/b/Y"
TIME_FORMAT = "H:i"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"
```

### 2.4 UNFOLD Settings Dictionary

```python
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "Cancun Airport Transportation (Admin)",
    "SITE_HEADER": "CAT (Admin)",
    "SITE_SUBHEADER": "Dashboard",
    "SITE_DROPDOWN": [
        {
            "icon": "web",
            "title": "Landing Page",
            "link": "https://cancunsairporttransportation.com/",
        },
    ],
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("favicon.png"),
    "SITE_LOGO": lambda request: static("logo.svg"),
    "SITE_SYMBOL": "blog",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon.png"),
            "attrs": {"target": "_blank"},
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": False,
    "ENVIRONMENT": "utils.callbacks.environment_callback",
    "ENVIRONMENT_TITLE_PREFIX": "utils.callbacks.environment_title_prefix_callback",
    "DASHBOARD_CALLBACK": "utils.callbacks.dashboard_callback",
    "THEME": "light",
    "LOGIN": {
        "redirect_after": lambda request: reverse_lazy("admin:APP_MODEL_changelist"),
    },
    "STYLES": [
        lambda request: static("css/style.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/script.js"),
        lambda request: static("js/add_tailwind_styles.js"),
    ],
    "COLORS": {
        "base": {
            "50": "oklch(98% .003 247)",
            "100": "oklch(96% .003 247)",
            "200": "oklch(91% .005 247)",
            "300": "oklch(84% .008 247)",
            "400": "oklch(68% .012 247)",
            "500": "oklch(54% .014 247)",
            "600": "oklch(44% .014 247)",
            "700": "oklch(36% .015 247)",
            "800": "oklch(28% .016 264)",
            "900": "oklch(22% .018 264)",
            "950": "oklch(16% .02 264)",
        },
        "primary": {
            "50": "oklch(97% .025 70)",
            "100": "oklch(94% .055 70)",
            "200": "oklch(89% .095 65)",
            "300": "oklch(82% .145 60)",
            "400": "oklch(75% .18 55)",
            "500": "oklch(70% .19 50)",
            "600": "oklch(62% .175 48)",
            "700": "oklch(53% .155 46)",
            "800": "oklch(45% .13 45)",
            "900": "oklch(38% .1 44)",
            "950": "oklch(28% .07 42)",
        },
    },
    "TABS": [
        {
            "models": ["auth.user", "auth.group"],
            "items": [
                {"title": _("Users"), "link": reverse_lazy("admin:auth_user_changelist")},
                {"title": _("Groups"), "link": reverse_lazy("admin:auth_group_changelist")},
            ],
        },
    ],
}
```

## 3. Custom Callbacks (`utils/callbacks.py`)

These functions provide dynamic information to the Unfold header and dashboard.

```python
import os

def environment_callback(request):
    env = os.getenv("ENV", "dev")
    env_mapping = {
        "prod": ["Production", "danger"],
        "staging": ["Staging", "warning"],
        "dev": ["Development", "info"],
        "local": ["Local", "success"],
    }
    return env_mapping.get(env, ["Unknown", "info"])

def environment_title_prefix_callback(request):
    env = os.getenv("ENV", "dev")
    prefix_mapping = {"prod": "[PROD]", "staging": "[STAGING]", "dev": "[DEV]", "local": "[LOCAL]"}
    return prefix_mapping.get(env, "[UNKNOWN]")

def dashboard_callback(request, context):
    context.update({"sample": "example"})
    return context
```

## 4. Admin Implementation (`project/admin.py`)

### 4.1 Customizing Default Auth Models

To apply Unfold to default models, you must unregister and re-register them using Unfold's classes:

```python
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
```

### 4.2 Base Admin Class (`ModelAdminUnfoldBase`)

```python
from unfold.admin import ModelAdmin
from unfold.decorators import action
from unfold.paginator import InfinitePaginator
from unfold.contrib.filters.admin import RangeDateFilter

class ModelAdminUnfoldBase(ModelAdmin):
    # UI Setup
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_sheet = False
    change_form_show_cancel_button = True
    
    # Pagination
    paginator = InfinitePaginator

    # Row Actions
    actions_row = ["edit"]

    def _get_base_actions_row(self):
        base_actions = ["edit"]
        child_actions = getattr(self, "actions_row", [])
        all_actions = base_actions + [a for a in child_actions if a not in base_actions]
        return [self.get_unfold_action(action) for action in all_actions]

    @action(description="Edit", permissions=["edit"], url_path="edit-post")
    def edit(self, request, object_id):
        return redirect(reverse(f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change", args=[object_id]))

    # Global Filters (Auto-apply to all models with these fields)
    global_filters = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
    )

    def get_list_filter(self, request):
        child_filters = super().get_list_filter(request) or []
        final_filters = list(child_filters)
        model_fields = [f.name for f in self.model._meta.get_fields()]

        for field_name, filter_class in self.global_filters:
            if field_name in model_fields and field_name not in str(final_filters):
                final_filters.append((field_name, filter_class))

        return final_filters
```

## 5. UI Assets & Customization

### 5.1 Template Override (`project/templates/admin/base.html`)

Used to load external libraries like SimpleMDE for Markdown:

```html
{% extends "admin/base.html" %}
{% load static %}
{% block extrahead %}
{{ block.super }}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css">
<script src="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.js"></script>
{% endblock %}
```

### 5.2 Dynamic Tailwind Injection (`static/js/add_tailwind_styles.js`)

Used to apply specific Tailwind classes to existing elements after page load:

```javascript
document.addEventListener("DOMContentLoaded", () => {
  const classes = [
    { selector: ".btn", classes: "bg-primary-600 block border border-transparent cursor-pointer font-medium px-3 py-2 rounded-default text-white w-full lg:w-auto flex items-center justify-center hover:bg-primary-700 hover:text-white transition-colors duration-300" },
    { selector: ".img-preview", classes: "w-auto h-16 rounded-xl object-cover" },
  ]
  classes.forEach(({ selector, classes }) => {
    document.querySelectorAll(selector).forEach(el => el.classList.add(...classes.split(" ")));
  });
});
```

### 5.3 Markdown Integration (`static/js/load_markdown.js`)

Initialized in `PostAdmin` via `class Media`:

```javascript
document.addEventListener("DOMContentLoaded", () => {
  const textAreas = document.querySelectorAll('div > textarea:not(#id_description)');
  setTimeout(() => {
    textAreas.forEach(textArea => {
      new SimpleMDE({ element: textArea, spellChecker: false });
    });
  }, 100);
});
```
