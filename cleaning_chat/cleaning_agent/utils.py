import random
import datetime

def get_api_date(service):
    # random date in the future in format YYYY-MM-DD HH:MM
    date=datetime.datetime.now() + datetime.timedelta( days=random.randint(1, 800), hours=random.randint(1, 12), minutes=random.randint(1, 60))
    date=date.strftime("%Y-%m-%d %H:%M")
    return date



    