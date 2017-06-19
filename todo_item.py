import datetime
import common


class TodoItem:

    def __init__(self, title, deadline):
        """
        Args:
            param1: title (string)
            param2: deadline (datetime.datetime object)

        """
        if type(title) != str:
            raise TypeError('Title must be a string')

        if type(deadline) != datetime.datetime:
            raise TypeError('Deadline must be a Datetime object')

        self.title = title
        self.deadline = deadline
        self.is_done = False

    def mark(self):
        self.is_done = True

    def unmark(self):
        self.is_done = False

    def __str__(self):
        marked_sign = '[x]' if self.is_done else '[ ]'
        formatted_date = common.get_day_month_format(str(self.deadline))
        output_message = '{} {} {}'.format(marked_sign, formatted_date, self.title)

        return output_message
