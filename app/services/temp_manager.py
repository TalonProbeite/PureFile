import uuid
import tempfile
from pathlib import Path
import shutil

def create_temp_dir() -> Path:
    """Creates a temporary directory with a project-specific prefix."""
    return Path(tempfile.mkdtemp(prefix="PureFile"))


def create_job_dir(temp_dir: Path) -> Path:
    """Creates a unique sub-directory for a specific processing job."""
    job_id = f"job_{uuid.uuid4()}"
    job_dir_path = temp_dir / job_id
    
    try:
        job_dir_path.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        """Handles potential issues with filesystem permissions or path limits."""
        print(f"Failed to create job directory: {error}")
        
    return job_dir_path


def delete_dir(path: Path) -> None:
    """Safely removes a directory and all its contents."""
    try:
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
    except PermissionError as error:
        """Handles cases where files are locked or access is denied."""
        print(f"Permission denied while deleting {path}: {error}")
    except Exception as error:
        print(f"Error while deleting directory {path}: {error}")