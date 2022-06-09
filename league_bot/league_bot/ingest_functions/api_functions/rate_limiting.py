from ratelimit import limits, sleep_and_retry



@sleep_and_retry
@limits(calls=98, period=120)
def limit_calls():
    """
    Call this function at the beginning of functions which need to be rate limited.
    """
    pass