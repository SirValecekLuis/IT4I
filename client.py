"""
This file serves as a client to test FastAPI server host locally.
"""

import time
import logging
import requests

URL = "http://localhost:8000"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_picture() -> str:
    req = f"{URL}/get_random_cat"
    response = requests.get(req, timeout=(0.001, None))

    if response.status_code == 200:
        return response.json()["task_id"]

    return "None"


def get_cat_status(task_id):
    logger.info(f"Checking status for task {task_id}")
    req = f"{URL}/get_random_cat_status?task_id={task_id}"
    try:
        start = time.time()
        response = requests.get(req, timeout=(0.001, None))
        response.raise_for_status()
        logger.info(f"Response from my FastAPI check cat status took {time.time() - start}s")
        data = response.json()
        logger.info(f"Status response from API: {data['status']}")
        return data
    except requests.RequestException as e:
        logger.error(f"Error getting task status: {str(e)}")
        return None


def main():
    """
    OUTPUT with 1.x s response from CAT API
    As we can see, both started at the same time and ended as well. So they were working async.
    INFO:__main__:Got task ID: 65d1ced4-12f9-4cb4-acf0-174bf5af0e8d
    INFO:__main__:Got task ID: aada9a51-05bc-44d9-916f-ce9b58be7148
    INFO:__main__:Checking status for task 65d1ced4-12f9-4cb4-acf0-174bf5af0e8d
    INFO:__main__:Response from my FastAPI check cat status took 0.014002323150634766s
    INFO:__main__:Status response from API: pending
    INFO:__main__:Checking status for task aada9a51-05bc-44d9-916f-ce9b58be7148
    INFO:__main__:Response from my FastAPI check cat status took 0.01400303840637207s
    INFO:__main__:Status response from API: pending
    INFO:__main__:Checking status for task 65d1ced4-12f9-4cb4-acf0-174bf5af0e8d
    INFO:__main__:Response from my FastAPI check cat status took 0.021550655364990234s
    INFO:__main__:Status response from API: pending
    INFO:__main__:Checking status for task aada9a51-05bc-44d9-916f-ce9b58be7148
    INFO:__main__:Response from my FastAPI check cat status took 0.01452493667602539s
    INFO:__main__:Status response from API: pending
    INFO:__main__:Checking status for task 65d1ced4-12f9-4cb4-acf0-174bf5af0e8d
    INFO:__main__:Response from my FastAPI check cat status took 0.012012958526611328s
    INFO:__main__:Status response from API: completed
    INFO:__main__:Checking status for task aada9a51-05bc-44d9-916f-ce9b58be7148
    INFO:__main__:Response from my FastAPI check cat status took 0.015528678894042969s
    INFO:__main__:Status response from API: completed
    INFO:__main__:Task completed. Result: https://cdn2.thecatapi.com/images/3k0.jpg
    INFO:__main__:Task completed. Result: https://cdn2.thecatapi.com/images/5pl.jpg
    """

    task_id = get_picture()
    task_id2 = get_picture()
    logger.info(f"Got task ID: {task_id}")
    logger.info(f"Got task ID: {task_id2}")
    for _ in range(10):
        status = get_cat_status(task_id)
        status2 = get_cat_status(task_id2)

        if status and status["status"] == "completed":
            logger.info(f"Task completed. Result: {status['result']}")
            task_id = ""

        if status2 and status2["status"] == "completed":
            logger.info(f"Task completed. Result: {status2['result']}")
            task_id2 = ""

        if task_id == "" and task_id2 == "":
            break
        time.sleep(0.5)
    else:
        logger.warning("Task did not complete in time")


if __name__ == "__main__":
    main()
