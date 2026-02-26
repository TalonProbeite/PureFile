import typing
from PIL import Image, ImageFile
import fitz
from docx import Document


MAX_META_STRING = 5000 


def get_ext(filename: str)->str:
    return filename.split('.')[-1].lower()


def get_metadata_img(file_obj: typing.BinaryIO)->dict:
     with Image.open(file_obj) as img:
        img.verify()
        file_obj.seek(0)
        with Image.open(file_obj) as f_img:
            return {"type": "image", "data": {str(k): str(v)[:MAX_META_STRING] for k, v in f_img.info.items()}}
        

def get_metadata_pdf(file_obj: typing.BinaryIO)->dict:
    with fitz.open(stream=file_obj.read(), filetype="pdf") as doc:
                return {"type": "pdf", "data": doc.metadata}
    


def get_metadata_docx(file_obj: typing.BinaryIO)->dict:
    doc = Document(file_obj)
    p = doc.core_properties
    return {
        "type": "docx",
        "data": {"author": p.author, "title": p.title, "last_modified_by": p.last_modified_by}
    }