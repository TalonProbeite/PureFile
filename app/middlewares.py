import time
from fastapi import Request
from loguru import logger


async def log_runtime_middleware(request:Request, call_next):
    start_time = time.perf_counter()
    
    
    response = await call_next(request)
    
    execute_time = time.perf_counter() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Time: {execute_time:.4f}s"
    )
    
    return response
