import io
import typing
from pathlib import Path

import fitz
from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile


class MetadataDeleteError(Exception):
    pass


def delete_metadata_docx(path:Path, output_path:Path|None=None) -> Path:

    if  output_path is None:
        output_path = path.parent / f"{path.stem}_clean{path.suffix}"
    
    try:
        doc = Document(path)
        core_props = doc.core_properties
        
        core_props.author = ""
        core_props.last_modified_by = ""
        core_props.title = ""
        core_props.subject = ""
        core_props.description = ""
        core_props.keywords = ""
        core_props.category = ""
        core_props.comments = ""
        core_props.content_status = ""
        core_props.identifier = ""
        core_props.language = ""
        core_props.version = ""
        
        doc.save(output_path)
        return output_path
    except (PackageNotFoundError , FileNotFoundError , OSError)as e:
        raise MetadataDeleteError from e


def delete_metadata_pdf(path:Path, output_path:Path|None=None) -> Path:

    if   output_path is None:
            output_path = path.parent / f"{path.stem}_clean{path.suffix}"

    try:

        with fitz.open(path) as doc:
            doc.set_metadata({})
            doc.del_xml_metadata()
            doc.save(output_path, garbage=4, deflate=True)
        
        return output_path
    except (fitz.FileNotFoundError , fitz.FileDataError , OSError) as e:
        raise MetadataDeleteError from e
    

async def delete_metadata_img(file: UploadFile, job_dir: Path, filename: str) -> Path:
    output_path = job_dir / filename
    
    try:
        data = b""
        data = await file.read()
        
        img = Image.open(io.BytesIO(data))
        clean = Image.new(img.mode, img.size)
        clean.putdata(list(img.getdata()))
        
        fmt = Path(filename).suffix.lstrip(".").upper()
        if fmt == "JPG":
            fmt = "JPEG"
        
        clean.save(output_path, format=fmt)
        return output_path
    
    except (UnidentifiedImageError, OSError, PermissionError) as e:
        raise MetadataDeleteError(str(e)) from e