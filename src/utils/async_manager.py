import asyncio
import logging


class AsyncManager:
    """
    A utility class for managing common asyncio tasks like retries and session management.
    """

    def __init__(self, semaphore_limit=10):
        self.semaphore = asyncio.Semaphore(semaphore_limit)

    async def process_tasks(self, tasks):
        """
        Manages asyncio tasks with concurrency limits.
        :param tasks: A list of coroutine tasks.
        """
        async with self.semaphore:
            await asyncio.gather(*tasks)

    async def retry_with_backoff(self, func, *args, retries=3, delay=1, **kwargs):
        """
        Executes a function with retries and exponential backoff.
        :param func: The async function to call.
        :param args: Positional arguments to pass to the function.
        :param retries: The maximum number of retry attempts.
        :param delay: The initial delay between retries.
        :param kwargs: Keyword arguments to pass to the function.
        :return: The result of the function if successful.
        :raises: The exception from the final failed attempt.
        """
        for attempt in range(retries):
            try:
                async with self.semaphore:
                    return await func(*args, **kwargs)

            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay * (2**attempt))  # Exponential backoff
                else:
                    logging.error("Retries exhausted. Raising exception.")
                    raise e
