from fastapi import APIRouter, UploadFile, File

from app.services import write_img_to_file, insert_doc_obj, get_doc_by_id, \
    delete_obj, insert_doc_text_obj, get_doc_text_by_id

from app.celery_task import img_to_text

import os


doc_router = APIRouter()


@doc_router.post(
    "/upload_doc/",
    tags=['Images'],
    description='Форматы: image/jpeg, image/png, image/jpg',
    summary='Загрузить картинку'
)
def upload_doc(file: UploadFile = File(...)):

    content_type = file.content_type

    if content_type not in {"image/jpeg", "image/png", "image/jpg"}:
        return {"error": "Invalid file type. Must be in (jpeg, jpg, png)"}

    path = write_img_to_file(file)
    insert_doc_obj(path)

    return {"info": f"file '{file.filename}' saved at '{path}'"}


@doc_router.get(
    "/doc_delete/",
    tags=['Documents'],
    description='Удалит запись по id из таблицы documents',
    summary='Удалить запись по id'
)
def doc_delete(id: int):
    doc = get_doc_by_id(id)

    if not doc:
        return {"error": f"There's no obj with id={id}"}

    delete_obj(doc)
    os.remove(doc.pasth)
    return {"info": f"file '{doc.pasth}' has deleted"}


@doc_router.get(
    "/doc_analyse/",
    tags=['Images'],
    description='Распознает текст с картинки по id и добавит в таблицу documents_text в БД',
    summary='Распознать текст с картинки'
)
def doc_analyse(id: int):
    doc = get_doc_by_id(id)

    if not doc:
        return {"error": f"There's no obj with id={id}"}

    text = img_to_text.delay(f'/fastapi/{doc.pasth}')
    insert_doc_text_obj(id_doc=id, text=text.get())

    return {"info": f"File with id={id} has analysed"}


@doc_router.get(
    "/get_text/",
    tags=['Documents text'],
    description='Вернет текст по id из таблицы documents_text в БД',
    summary='Вернуть текст по id'
)
def get_text(id: int):
    doc_text = get_doc_text_by_id(id)

    if not doc_text:
        return {"error": f"There's no obj with id={id}"}
    return {f"text by id={id}": doc_text.text}


@doc_router.get(
    "/",
    description='Проверка работоспособности приложения',
    summary='«status»: True'
)
def check_app():
    return {"status": True}
