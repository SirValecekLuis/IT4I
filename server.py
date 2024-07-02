"""
This file serves as server run locally to test FastAPI.
"""

import time
import logging
import uvicorn
from fastapi import FastAPI

from tasks import celery_app, get_random_cat_task

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/get_random_cat")
async def get_random_cat() -> dict:
    start = time.time()
    try:
        task = get_random_cat_task.delay()
        logger.info(f"API get_random_cat took {time.time() - start} to finish")
        return {"task_id": task.id}
    except Exception as e:
        logger.error(f"Task error while putting task in queue {e}")
        logger.info(f"API get_random_cat took {time.time() - start} to finish")


@app.get("/get_random_cat_status")
async def get_random_cat_status(task_id: str) -> dict:
    start = time.time()
    try:
        task = celery_app.AsyncResult(task_id)
        logger.info(f"Task id {task_id}: {task.state}")
        if task.state == "PENDING":
            logger.info(f"API get_random_cat_status took {time.time() - start} to finish")
            return {"status": "pending"}

        if task.state == "FAILURE":
            logger.info(f"API get_random_cat_status took {time.time() - start} to finish")
            return {"status": "failed", "error": str(task.result)}

        if task.successful():
            logger.info(f"API get_random_cat_status took {time.time() - start} to finish")
            return {"status": "completed", "result": task.result}

        logger.info(f"API get_random_cat_status took {time.time() - start} to finish")
        return {"status": task.state}
    except Exception as e:
        logger.info(f"API get_random_cat_status took {time.time() - start} to finish")
        logger.error(f"Task id {task_id}: Error")
        return {"status": "error", "error": str(e)}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
