from todo_item import TodoItem
from todo_quarter import TodoQuarter
import common
import datetime
import csv
import ui


class TodoMatrix:
    Quarters_names = ['IU', 'IN', 'NU', 'NN']

    def __init__(self):
        self.todo_quarters = {}
        for name in TodoMatrix.Quarters_names:
            self.todo_quarters[name] = TodoQuarter()

    def add_items_from_file(self, file_name):
        try:
            data = self.__read_file(file_name)

        except FileNotFoundError:
            raise FileNotFoundError('This file does not exist in provided directory.')

        TodoMatrix.__add_item_manager(self, data)

    def __read_file(self, file_name):
        temp = []

        with open(file_name, 'r') as csvfile:
            file_reader = csv.reader(csvfile)

            for record in file_reader:
                temp.append(record[0].split('|'))

        return temp

    def add_item(self, title, deadline, is_important=False):
        if type(deadline) != datetime.datetime:
            raise TypeError('Incorrect deadline')

        deadline = common.get_day_month_format(deadline)
        data = [[title, deadline, is_important]]

        TodoMatrix.__add_item_manager(self, data)

    def __add_item_manager(self, data):
        """
        This function get specified package of variables and then add to
        appropriate object.

        Args:
            param1: data (list)

        """
        actual_date = datetime.date.today()
        quarter = {(True, True): 'IU', (True, False): 'IN', (False, True): 'NU', (False, False): 'NN'}

        for record in data:
            priorities = self.__check_priority(record, actual_date)
            assigned_quarter = (priorities['is_important'], priorities['is_urgent'])
            day, month = self.__get_values_for_datetime_object(record[1])
            deadline = datetime.datetime(2017, int(month), int(day))

            self.todo_quarters[quarter[assigned_quarter]].add_item(record[0], deadline)

    def __check_priority(self, record, actual_date):
        is_important = record[2]
        is_urgent = self.__check_is_task_urgent(record[1], actual_date)
        priority = {'is_important': False, 'is_urgent': False}

        if is_important:
            priority['is_important'] = True

        if is_urgent:
            priority['is_urgent'] = True

        return priority

    def __check_is_task_urgent(self, task_end_date, actual_date):
        if type(task_end_date) == str:
            day, month = self.__get_values_for_datetime_object(task_end_date)
            task_end_date = datetime.date(2017, int(month), int(day))

        is_urgent = False
        delta = task_end_date - actual_date

        if delta.days <= 3:
            is_urgent = True

        return is_urgent

    def __get_values_for_datetime_object(self, end_date):
        # read values from DD_MM date type, which is provided with data loading
        # from file
        separator_index = end_date.index('-')
        day = end_date[:separator_index]
        month = end_date[separator_index+1:]

        return day, month

    def archive_items(self):
        # deleting done tasks
        for quarter in self.todo_quarters:
            self.todo_quarters[quarter].archive_items()

    def save_items_to_file(self, file_name):
        temp_data_storage = []

        # get formated data from every quarter
        for quarter in self.todo_quarters:
            temp_data_storage.extend(self.__get_formatted_data(quarter))

        self.__save_file(file_name, temp_data_storage)

    def __get_formatted_data(self, quarter):
        temp = []

        for task in self.todo_quarters[quarter].todo_items:
            deadline = common.get_day_month_format(task.deadline)

            if quarter[0] == 'I':
                formated_data = task.title + '|' + deadline + '|' + 'important'

            else:
                formated_data = task.title + '|' + deadline + '|' + ''

            temp.append(formated_data)

        return temp

    def __save_file(self, file_name, data):
        with open(file_name, 'w') as csvfile:
            file_writer = csv.writer(csvfile)

            for record in data:
                file_writer.writerow([record])

    def get_quarter(self, status):
        return self.todo_quarters[status]
