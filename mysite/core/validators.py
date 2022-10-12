from django.core.exceptions import ValidationError


def validate_icon_size(value):
    """
    Do not allow icon images larger than 0.5MB
    """
    image_size = value.size
    if image_size > 0.5 * 1024 * 1024:
        raise ValidationError("The maximum file size that can be uploaded is 500kB")
    else:
        return value
