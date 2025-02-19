from setupDatabase import check_database_created
import logging
logging.basicConfig(filename='library.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def setup():
    logger.info("Setup running")
    check_database_created()

setup()