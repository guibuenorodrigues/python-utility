import retries


@retries.retry(exceptions=(ZeroDivisionError, Exception), retries=3, delay=1, backoff=2)
def main(dividend: float, divisor: float) -> None:
    try:
        if divisor < 0:
            raise Exception("DIVISOR cannot be less than zero")

        result = dividend / divisor
        print(f"{dividend} / {divisor} = {result}")

    except ZeroDivisionError as e:
        raise e
    except Exception as e:
        raise e


if __name__ == "__main__":
    main(dividend=1, divisor=0)
