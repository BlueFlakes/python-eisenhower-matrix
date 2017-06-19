from todo_item import TodoItem
from datetime import datetime


def add_attr_date_as_key_value(array):
    """
    add new attribute date which is easyer to interpret by sorting function

    Args:
        param1: array (list of objects)

    Returns:
        array (list of objects)
    """
    for struct in array:
        new_date_format = int(str(struct.deadline)[5:7]+str(struct.deadline)[8:10])
        struct.new_date_format = new_date_format

    return array


class TodoQuarter:

    def __init__(self):
        self.todo_items = []

    def add_item(self, title, deadline):
        self.todo_items.append(TodoItem(title, deadline))
        TodoQuarter.sort_items(self)

    def sort_items(self):
        array = add_attr_date_as_key_value(self.todo_items)

        for i in range(len(array)):
            for j in range(i, len(array)):

                if array[i].new_date_format > array[j].new_date_format:
                    temp_value = array[i]
                    array[i] = array[j]
                    array[j] = temp_value

        for struct in array:
            del struct.new_date_format

        self.todo_items = array

    def remove_item(self, index):
        if index not in range(0, len(self.todo_items)):
            raise IndexError('Out of range.')

        del self.todo_items[index]

    def archive_items(self):
        item_index = 0

        while item_index < len(self.todo_items):
            if self.todo_items[item_index].is_done is True:
                del self.todo_items[item_index]
                item_index -= 1

            item_index += 1

    def get_tasks_amount(self):
        return len(self.todo_items)

    def get_item(self, index):
        if index not in range(0, len(self.todo_items)):
            raise IndexError('Out of range.')

        return self.todo_items[index]

    def __str__(self):
        strings_sum = ''

        for i in range(len(self.todo_items)):
            strings_sum += '{}. {}\n'.format(str(i+1), self.todo_items[i].__str__())

        return strings_sum
