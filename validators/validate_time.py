from datetime import datetime

def check_time_format(time_input):
    try:
        datetime.fromisoformat(time_input.replace('Z', '+00:00'))
    except:
        return False
    return True