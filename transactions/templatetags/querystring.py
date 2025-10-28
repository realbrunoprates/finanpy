from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def update_query(context, **kwargs):
    """
    Build a querystring using current request GET parameters and overrides.
    """
    request = context.get('request')

    if request is None:
        return ''

    query_params = request.GET.copy()

    for key, value in kwargs.items():
        if value is None:
            query_params.pop(key, None)
        else:
            query_params[key] = value

    return query_params.urlencode()
