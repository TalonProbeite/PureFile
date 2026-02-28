from fastapi import APIRouter , UploadFile , HTTPException , Request , BackgroundTasks
from loguru import logger
from fastapi.responses import FileResponse

from ..services.metadata_read import get_ext , get_metadata_docx , get_metadata_img , get_metadata_pdf , MetadataReadError
from ..services.metadata_delete import delete_metadata_docx , delete_metadata_img , delete_metadata_pdf , MetadataDeleteError
from ..services.temp_manager import create_job_dir , delete_dir

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
            logger.info(f"Processed file type: {ext.upper()}")
            return result
        except MetadataReadError as e:
            original_err_name = type(e.__cause__).__name__ if e.__cause__ else "UnknownError"
            

            logger.bind(
                original_exception=original_err_name,
                filename=upload_file.filename
            ).exception(f"Failed to read metadata from {ext} file")
            
            raise HTTPException(status_code=415, detail="Corrupted file or invalid file format. Only PDF, Docx, PNG,  JPG , JPEG formats are supported.")




@router.post("/delete_metadata")
async def delete_metadata(background_tasks: BackgroundTasks, request: Request, upload_file: UploadFile):
    if request.app.state.temp_dir is None:
        raise HTTPException(status_code=501, detail="Temporary directory is not available")
    
    if not upload_file.filename:
        raise HTTPException(status_code=400, detail="File name is missing")
    
    media_types = {
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
    }
    
    ext = get_ext(upload_file.filename)
    job_dir = create_job_dir(request.app.state.temp_dir)
    
    if job_dir is None:
        raise HTTPException(status_code=500, detail="Failed to create job directory")
    
    try:
        match ext:
            case "png" | "jpg" | "jpeg":
                result = await delete_metadata_img(upload_file, job_dir, upload_file.filename)
            case "pdf":
                save_path = job_dir / upload_file.filename
                with open(save_path, "wb") as f:
                    while chunk := await upload_file.read(1024 * 1024):
                        f.write(chunk)
                result = delete_metadata_pdf(save_path)
            case "docx":
                save_path = job_dir / upload_file.filename
                with open(save_path, "wb") as f:
                    while chunk := await upload_file.read(1024 * 1024):
                        f.write(chunk)
                result = delete_metadata_docx(save_path)
            case _:
                raise HTTPException(status_code=422, detail="Incorrect data format. Only pdf, docx, png, jpg, jpeg are supported.")
        
        logger.info(f"Processed file type (delete): {ext.upper()}")
        return FileResponse(
            result,
            media_type=media_types[ext],
            filename=f"clean_{upload_file.filename}",
            background=background_tasks.add_task(delete_dir, job_dir)
        )
    except MetadataDeleteError as e:
        background_tasks.add_task(delete_dir, job_dir)
        original_err_name = type(e.__cause__).__name__ if e.__cause__ else "UnknownError"
        
        logger.bind(
            original_exception=original_err_name,
            filename=upload_file.filename
        ).exception(f"Failed to delete metadata from {ext} file")
        
        raise HTTPException(status_code=415, detail="Corrupted file or invalid file format. Only PDF, Docx, PNG, JPG, JPEG formats are supported.")
