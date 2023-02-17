from time import perf_counter
from typing import Any, Callable
import logging
import functools


logger = logging.getLogger("my_app")


def benchmark_old(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        logging.info(
            f"Execution of {func.__name__} took {run_time:.2f} seconds.")

    return wrapper


def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        logging.info(
            f"Execution of {func.__name__} took {run_time:.2f} seconds to execute")
        return value

    return wrapper


def with_logging(func: Callable[..., Any], logger: logging.Logger) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f"Calling {func.__name__}")
        value = func(*args, **kwargs)
        logger.info(f"Successfully called {func.__name__}")
        return value

    return wrapper


with_default_logging = functools.partial(with_logging, logger=logger)


@with_default_logging()
@benchmark
def pow_2(number: int | float) -> int | float:
    return number ** 2


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    value = pow_2(104)

    print(value)
