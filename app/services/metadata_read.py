import typing
from PIL import Image, ImageFile , UnidentifiedImageError 
import fitz
from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from zipfile import BadZipFile


MAX_META_STRING = 5000 


class MetadataReadError(Exception):
    pass


def get_ext(filename: str)->str:
    return filename.split('.')[-1].lower()


def get_metadata_img(file_obj: typing.BinaryIO)->dict:
    try:
        with Image.open(file_obj) as img:
            img.verify()
            file_obj.seek(0)
            with Image.open(file_obj) as f_img:
                return {"type": "image", "data": {str(k): str(v)[:MAX_META_STRING] for k, v in f_img.info.items()}}
    except (UnidentifiedImageError , OSError) as e:
         raise MetadataReadError from e
            

def get_metadata_pdf(file_obj: typing.BinaryIO)->dict:
    try: 
        with fitz.open(stream=file_obj.read(), filetype="pdf") as doc:
                return {"type": "pdf", "data": doc.metadata}
    except (RuntimeError , ValueError)as e:
         raise MetadataReadError from e
    


def get_metadata_docx(file_obj: typing.BinaryIO)->dict:
    try:
        doc = Document(file_obj)
        p = doc.core_properties
        return {
            "type": "docx",
            "data": {"author": p.author, "title": p.title, "last_modified_by": p.last_modified_by}
        }
    except (BadZipFile , PackageNotFoundError , KeyError) as e:
        raise MetadataReadError from e
