import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

try:
    logger.info("Trying to divide 0 by 0!")
    print(0 / 0)
except Exception as e:
    print(e)
    logger.error("Oops")
