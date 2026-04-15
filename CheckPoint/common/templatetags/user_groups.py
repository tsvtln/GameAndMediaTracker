from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()


@register.filter(name='in_groups')
def in_groups(user, groups):
    if not user.is_authenticated:
        return False
    group_list = [g.strip() for g in groups.split(',')]
    return user.groups.filter(name__in=group_list).exists()


@register.filter(name='filename')
def filename(file_path):
    if hasattr(file_path, 'name'):
        return file_path.name.split('/')[-1]
    return str(file_path).split('/')[-1]


@register.filter(name='get_item')
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)

