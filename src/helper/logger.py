import logging
import os

# Configure logging

log_path = os.path.join(os.path.dirname(__file__), "..","..","logs", "server.log")
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log(tag : str, message) :
    match tag:
        case "INFO" :
            logging.info(message)
        case "WARNING" :
            logging.warning(message)
        case "ERROR" : 
            logging.error(message)