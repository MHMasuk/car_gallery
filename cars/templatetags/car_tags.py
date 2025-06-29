from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def features_as_list(features_text):
    """
    Convert a comma-separated features text into a formatted HTML list.

    Usage: {{ car.features|features_as_list }}
    """
    if not features_text:
        return mark_safe('<p class="text-muted">No specific features listed for this vehicle.</p>')

    # Split by commas and clean up each feature
    features = [feature.strip() for feature in features_text.split(',') if feature.strip()]

    # Build HTML
    html = '<div class="row">'
    for feature in features:
        html += '''
        <div class="col-md-6 mb-2">
            <div class="d-flex align-items-center">
                <i class="fas fa-check-circle text-success me-2"></i>
                <span>{}</span>
            </div>
        </div>
        '''.format(feature)
    html += '</div>'

    return mark_safe(html)


@register.filter
def addclass(field, css_class):
    """
    Add a CSS class to a form field.

    Usage: {{ form.field|addclass:"form-control" }}
    """
    return field.as_widget(attrs={'class': css_class})