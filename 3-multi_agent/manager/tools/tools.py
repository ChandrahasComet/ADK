import datetime

def get_current_time(format: str)->dict:
    """
    Get the current time in the mentioned format.
    """
    return {
        "current_time": datetime.datetime.now().strftime(format) if format else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
