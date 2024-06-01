from django import template

import re

register = template.Library()


@register.filter('get_name_by_url')
def get_name_by_url(url):
    pattern = r"https://([^/]+)/"

    match = re.search(pattern, url)

    return match.group(1)


@register.filter('bootstrap_status')
def bootstrap_status(status):
    data = {
        'CO': 'bg-success text-white',
        'PE': 'bg-warning',
        'BA': 'bg-info',
        'PA': 'bg-info',
        'IP': 'bg-primary text-white',
        'CA': 'bg-danger text-white'
    }

    return data[status]
