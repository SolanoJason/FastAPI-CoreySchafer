from fastapi import UploadFile
from PIL import Image
from typing import Annotated
from pydantic import AfterValidator


def validate_image(upload: UploadFile | None) -> UploadFile | None:
    if upload is None:
        return None

    try:
        upload.file.seek(0)
        with Image.open(upload.file) as image:
            image.verify()
    except (OSError, ValueError) as error:
        raise ValueError("The uploaded file is not a valid image") from error
    finally:
        upload.file.seek(0)

    return upload

ImageUploadFile = Annotated[UploadFile, AfterValidator(validate_image)]