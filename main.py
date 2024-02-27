from app.views import doc_router
from fastapi import FastAPI
# import uvicorn

description = """
API для распознования и хранение текста с картинки. 🚀

## Images

#### Метод: /upload_doc/<br>
* Загрузите картинку. **Форматы: image/jpeg, image/png, image/jpg**<br>
* Она сохранится в проекте, в папке **documents**.<br>
* Создатся объект модели **Documents**.<br>
* Добавиться запись в таблицу **documents** в БД.

#### Метод: /doc_analyse/{id: int}<br>
* Достанет объект из БД, из таблицы **documents** по **id**.<br>
* Возьмет картинку и распознает текст, используя **Tesseract**.<br>
* Создаст объект модели **Documents_text** с текстом.<br>
* Добавит в таблицу **documents_text** В БД.<br>
* Все действия происходят в фоновом режиме, мспользуя **Celery и RabbitMQ**.

## Documents

#### Метод: /doc_delete/{id: int}<br>
* Удалит запись в таблице **documents** по **id**

## Documents_text

#### Метод: /get_text/{id: int}<br>
* Вернет текст из таблицы **documents_text** по **id**
"""

app = FastAPI(
    title='Documents App',
    description=description,
    contact={
        "name": "Kirill Rakhno",
        "url": "https://t.me/Kiryarah",
        "email": "kiryarah@gmail.com",
    },
)

app.include_router(doc_router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
