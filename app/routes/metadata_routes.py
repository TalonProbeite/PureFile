from fastapi import APIRouter , UploadFile , HTTPException
from loguru import logger

from ..services.metadata import get_ext , get_metadata_docx , get_metadata_img , get_metadata_pdf , MetadataReadError


router = APIRouter( tags=["read_metadata"])



@router.post("/read_metadata")
async def get_metadata(upload_file: UploadFile)->dict:
        if not upload_file.filename:
            raise HTTPException(status_code=400, detail="File name is missing")
        
        ext = get_ext(upload_file.filename)
        try:
            match ext:
                    case "png" | "jpg" | "jpeg":
                        result = get_metadata_img(upload_file.file)
                    case "pdf":
                        result = get_metadata_pdf(upload_file.file)
                    case "docx":
                        result = get_metadata_docx(upload_file.file)
                    case _:
                        raise HTTPException(status_code=422, detail="Incorrect data format. Only pdf, docx, png, jpg , jpeg are supported.")
            return result
        except MetadataReadError as e:
            original_err_name = type(e.__cause__).__name__ if e.__cause__ else "UnknownError"
            

            logger.bind(
                original_exception=original_err_name,
                filename=upload_file.filename
            ).exception(f"Failed to read metadata from {ext} file")
            
            raise HTTPException(status_code=415, detail="Corrupted file or invalid file format. Only PDF, Docx, PNG,  JPG , JPEG formats are supported.")