import functools
import logging
import time
from typing import Callable, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def retry(
    backoff: int = 1,
    retries: int = 3,
    delay: int = 5,
    exceptions: Tuple = (Exception,),
    disable_logs: bool = False,
) -> Callable:
    """
    A decorator that retries a function call with an exponential backoff.

    Parameters:
    backoff (int): The factor by which the delay increases after each retry. Default is 1 (no backoff).
    retries (int): The number of retry attempts. Default is 3.
    delay (int): The initial delay between retries in seconds. Default is 2 seconds.
    exceptions (Tuple): A tuple of exception types to trigger a retry. Default is (Exception,).
    disable_logs (bool): Disable all logs and prints.

    Returns:
    Callable: The decorated function with retry logic.

    Example:
    @retry(retries=5, delay=1, backoff=2, exceptions=(ValueError,))
    def test_function():
        print("Trying...")
        raise ValueError("An error occurred")

    try:
        test_function()
    except Exception as e:
        print(e)
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            current_delay = delay
            current_exception = None

            for attempt in range(retries):
                starting_time = time.perf_counter()
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if not disable_logs:
                        logger.warning(f"attempt {attempt + 1} failed: {e}")

                    current_exception = e

                    time.sleep(current_delay)
                    current_delay *= backoff

                end_time = time.perf_counter()

                if not disable_logs:
                    logger.info(
                        f"attempt {attempt + 1} took {end_time - starting_time}"
                    )

            raise Exception(
                f"function {func.__name__} failed after {retries} retries. Exc: {str(current_exception)}"
            )

        return wrapper_func

    return decorator
