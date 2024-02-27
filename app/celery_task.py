import pytesseract
from PIL import Image
from settings import make_celery


celery = make_celery()


@celery.task
def img_to_text(img_url: str, lang: str = 'rus') -> str:
    image = Image.open(img_url)
    return pytesseract.image_to_string(image=image, lang=lang)
