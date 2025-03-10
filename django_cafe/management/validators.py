import os
from django.core.exceptions import ValidationError


def validate_file_extension(file):
    if file:
        extension = os.path.splitext(file.name)[1]
        if extension not in {".jpeg", ".png", ".webp"}:
            raise ValidationError("Invalid file format. Supported file formats are jpeg | png | webp")

    return file
