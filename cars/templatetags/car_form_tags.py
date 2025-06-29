from django import template
from django.forms.widgets import CheckboxInput, FileInput

register = template.Library()

@register.filter
def is_checkbox(field):
    """
    Check if the form field is a checkbox
    """
    return isinstance(field.field.widget, CheckboxInput)

@register.filter
def is_file_input(field):
    """
    Check if the form field is a file input
    """
    return isinstance(field.field.widget, FileInput)

@register.filter
def add_class(field, css_class):
    """
    Add a CSS class to the field
    """
    return field.as_widget(attrs={"class": f"{field.css_classes()} {css_class}"})
