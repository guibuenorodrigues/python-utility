import retries

"""Retry for any raised exception"""


@retries.retry()
def main():
    try:
        return 1 / 0
    except Exception:
        raise


if __name__ == "__main__":
    main()
