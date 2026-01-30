# utils/callbacks/environment_callback.py
import os


def environment_callback(request):
    """
    Callback has to return a list of two values representing:
    - Text value (the environment name)
    - Color type of the label: "info", "danger", "warning", "success"
    """
    env = os.getenv("ENV", "dev")

    # Map environment to display text and color
    env_mapping = {
        "prod": ["Production", "danger"],  # Red - indicates caution
        "staging": ["Staging", "warning"],  # Orange/Yellow
        "dev": ["Development", "info"],  # Blue - informational
        "local": ["Local", "success"],  # Green - safe
    }

    return env_mapping.get(env, ["Unknown", "info"])


def environment_title_prefix_callback(request):
    """
    Callback that returns a string prefix for the browser title tag.
    This appears before the page title, e.g., "[Production] - Dashboard"
    """
    env = os.getenv("ENV", "dev")

    # Map environment to title prefix
    prefix_mapping = {
        "prod": "[PROD]",
        "staging": "[STAGING]",
        "dev": "[DEV]",
        "local": "[LOCAL]",
    }

    return prefix_mapping.get(env, "[UNKNOWN]")


def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is used as dashboard
    template. It can be overridden in application by creating custom admin/index.html.
    """
    context.update(
        {
            "sample": "example",  # this will be injected into templates/admin/index.html
        }
    )
    return context
