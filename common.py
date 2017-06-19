# This module is designed to store common functions


def get_day_month_format(deadline):
    """
    Getting from object date and modify itself to expected format.

    Args:
        param1: deadline (datetime.datetime object)

    Return:
        deadline (string) formated day in DD_MM style
    """
    deadline = str(deadline)
    deadline = str(int(deadline[8:10])) + '-' + str(int(deadline[5:7]))

    return deadline
