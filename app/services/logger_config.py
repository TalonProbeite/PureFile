import sys
from loguru import logger

def setup_logging():
    logger.remove()

    logger.level("INFO", color="<blue>")
    logger.level("DEBUG", color="<green>")
    logger.level("ERROR", color="<red>")

  
    logger.add(
        sys.stdout,
        format="<level>{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | IP: {extra[client_ip]} | {message}</level>",
        colorize=True,
        level="DEBUG"
    )

    logger.add(
        "logs/errors.json", 
        level="ERROR", 
        serialize=True,
        rotation="10 MB"
    )


    logger.add(
        "logs/info.json", 
        level="INFO", 
        compression="zip", 
        rotation="10 KB", 
        serialize=True, 
        retention="1 week"
    )


    logger.configure(extra={"client_ip": "system"}) 