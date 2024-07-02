"""
This file serves for celery functions called in server.py.
"""

import logging
import os
import time
import requests

from celery import Celery

# 3 hours of debugging, because windows needs this -> --pool=solo
# Or just use the os.environ which enables multiprocessing
# celery -A tasks worker --pool=solo -l info
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
celery_app = Celery("tasks",
                    broker="redis://host.docker.internal:6379/0",
                    backend="redis://host.docker.internal:6379/1")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.get_random_cat_task", bind=True)
def get_random_cat_task(self) -> str:
    start = time.time()
    logger.info(f"Task {self.request.id} started")
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search", timeout=(0.2, None))
        response.raise_for_status()
        cat_data = response.json()[0]
        image_url = cat_data["url"]
        logger.info(f"Task {self.request.id} completed successfully in {time.time() - start}s")
        return image_url
    except Exception as e:
        logger.error(f"Task {self.request.id} failed: {str(e)}")
        return "None"
