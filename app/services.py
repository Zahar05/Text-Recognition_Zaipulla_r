from settings import session_db
from app.models import GeneralBase, Document, Document_text
from fastapi import UploadFile


def write_img_to_file(file: UploadFile):
    path = f'documents/{file.filename}'

    with open(path, 'wb') as img:
        img.write(file.file.read())

    return path


def _get_obj(base_class: GeneralBase, id: int):
    with session_db() as session:
        obj = session.get(base_class, id)
    return obj


def get_doc_by_id(id: int):
    return _get_obj(Document, id)


def get_doc_text_by_id(id: int):
    return _get_obj(Document_text, id)


def delete_obj(doc: GeneralBase):
    with session_db() as session:
        session.delete(doc)
        session.commit()


def _insert_obj(obj: GeneralBase):
    with session_db() as session:
        session.add(obj)
        session.commit()


def insert_doc_obj(path: str):
    _insert_obj(Document(pasth=path))


def insert_doc_text_obj(id_doc: int, text: str):
    _insert_obj(Document_text(id_doc=id_doc, text=text))
