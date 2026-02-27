import uuid
import tempfile
from pathlib import Path
import shutil
from loguru import logger


def create_temp_dir() -> Path | None:
    """Creates a temporary directory with a project-specific prefix."""
    try:
        temp_dir = Path(tempfile.mkdtemp(prefix="PureFile"))
        logger.info(f"A temporary directory has been created: {temp_dir}")
        return temp_dir
    except OSError as e:
        logger.error(f"Failed to create temporary directory : {e}")
        return None
   


def create_job_dir(temp_dir: Path) -> Path | None:
    """Creates a unique sub-directory for a specific processing job."""
    job_id = f"job_{uuid.uuid4()}"
    job_dir_path = temp_dir / job_id
    
    try:
        job_dir_path.mkdir(parents=True, exist_ok=True)
        return job_dir_path
    except OSError as e:
        """Handles potential issues with filesystem permissions or path limits."""
        logger.error(f"Failed to create temporary work directory: {e}")
        return None
        
    


def delete_dir(path: Path) -> None:
    """Safely removes a directory and all its contents."""
    try:
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
    except PermissionError as error:
        """Handles cases where files are locked or access is denied."""
        logger.error(f"Permission denied while deleting {path}: {error}")
    except Exception as error:
        logger.error((f"Error while deleting directory {path}: {error}"))