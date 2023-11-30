from mimetypes import MimeTypes

from django.conf import settings
from django.http import FileResponse


__all__ = []


def download_image(request, path):
    image_path = settings.MEDIA_ROOT / path
    content_type, encoding = MimeTypes().guess_type(image_path)
    return FileResponse(
        open(image_path, "rb"),
        content_type=content_type,
        as_attachment=True,
    )
