import ui
from todo_matrix import TodoMatrix
import calendar
import datetime
import os
from time import sleep


def choose_option(matrix):
    user_input = ui.get_inputs(['What do you want to do'])[0]

    if user_input == '1':
        get_quarter_status(matrix)
    elif user_input == '2':
        add_item(matrix)
    elif user_input == '3':
        universal_body(matrix, 'mark_mode')
    elif user_input == '4':
        universal_body(matrix, 'remove_mode')
    elif user_input == '5':
        archive_items(matrix)
    elif user_input == '6':
        print_table(matrix)

    return user_input


def handle_menu(menu):
    title = 'Eisenhower matrix menu:'
    exit_message = 'Exit'
    ui.print_menu(title, menu, exit_message)


def start_module():
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.

    Returns:
        None
    """
    menu = ['Show items by status', 'Add item', 'Enter task toggle mode',
            'Remove task', 'Archive Tasks', 'show eisenhower table']
    user_input = None
    matrix = TodoMatrix()
    try:
        matrix.add_items_from_file('my_file.csv')
    except FileNotFoundError:
        print("Error: file with data no provided.")
        open('my_file.csv', 'w').close()

    while user_input != '0':
        handle_menu(menu)
        user_input = choose_option(matrix)

    matrix.archive_items()
    matrix.save_items_to_file('my_file.csv')


def get_quarter_status(matrix, get_input_returned=False):
    title = 'Available status:'
    available_status = ['IU', 'IN', 'NU', 'NN']
    menu = ['"IU" - urgent & important items', '"IN" - not urgent & important items',
            '"NU" - urgent & not important items', '"NN" - not urgent & not important items']
    user_input = None

    while user_input not in available_status:
        ui.print_menu(title, menu, '', False)
        user_input = ui.get_inputs(['Please enter the status you chose'])[0].upper()

        if user_input not in available_status:
            ui.print_error_message('Wrong pick.')

    if not get_input_returned:
        show_items(matrix, user_input)

    if get_input_returned:
        return user_input


def show_items(matrix, user_input):
    """
    Print out tasks which are stored in specified quarter

    Args:
        param1: user_input (str) indicate which quarter have to be shown

    """
    if len(matrix.get_quarter(user_input).todo_items) > 0:
        ui.print_result(matrix.get_quarter(user_input).__str__(), 'get_quarter')

    else:
        ui.print_error_message('This space is empty.')


def get_expected_type(user_input, expected_user_input_type):
    if expected_user_input_type == int:
        try:
            user_input = int(user_input)

        except ValueError:
            ui.print_error_message('Wrong value provided.')

    return user_input


def additional_specific_conditions(step, user_input, user_answers):
    """
    Here are defined additional conditions for analysing date

    Args:
        param1: step (iter) it is progressing iterator of loop
        param2: user_input (int/str)
        param3: user_answers (int) get the value of maximum value of days in month

    Return:
        user_input (int/str/none) depends on the user input

    """
    if step == 1:
        # Make sure that the month number is in range of months in year
        if type(user_input) == int and user_input not in range(1, 13):
            ui.print_error_message('Out of range.')
            user_input = None

    elif step == 2:
        # Make sure that the day number is in range of available days in month
        month_number = user_answers['Month_number'] - 1
        days_in_month = calendar.mdays[1:][month_number]

        if type(user_input) == int and user_input not in range(1, days_in_month+1):
            ui.print_error_message('Out of range.')
            user_input = None

    elif step == 3:
        if user_input.lower() not in ['yes', 'no']:
            ui.print_error_message('Wrong answer.')
            user_input = None

        # Modify input to empty string because expected type is string and
        # we need string which represent bool value False
        elif user_input.lower() == 'no':
            user_input = ''

    return user_input


def add_item(matrix):
    """
    Here we have item manager, which  mostly is used for comparing
    type of user_input and expected type of user_input

    Args:
        param1: matrix (TodoMatrix object)

    """
    user_data = {}
    answers_keys = ['Title', 'Month_number', 'Day_number', 'Is important']
    questions = [['Title'], ['Month'], ['Day of month'], ['Is important(type yes or no)']]
    expected_answers_types = [str, int, int, str]

    for step in range(len(questions)):
        user_input = None

        while type(user_input) != expected_answers_types[step]:

            user_input = ui.get_inputs(questions[step])[0]
            user_input = get_expected_type(user_input, expected_answers_types[step])

            user_input = additional_specific_conditions(step, user_input, user_data)

        user_data[answers_keys[step]] = user_input

    datetime_object = datetime.datetime(2017, user_data['Month_number'], user_data['Day_number'])
    matrix.add_item(user_data['Title'], datetime_object, user_data['Is important'])


def is_index_in_range(matrix, records_amount):
    """
    Here are defined additional conditions for analysing date

    Args:
        param1: matrix (TodoMatrix object)
        param2: records_amount (int) amount of tasks in quarter

    Return:
        record_index (dict)

    """
    record_index = ui.get_inputs(['Which record to select'])[0]
    record_index = get_expected_type(record_index, int)
    record_index = {'index': record_index, 'in_range': False}

    if type(record_index['index']) == int:
        record_index['index'] -= 1

        if record_index['index'] in range(0, records_amount):
            record_index['in_range'] = True

        else:
            ui.print_error_message('Out of range.')

    return record_index


def toggle_mark(matrix, record_index, user_input, mode):
    """
    Toggle the status of task, between done and undone.

    Args:
        param1: matrix (TodoMatrix object)
        param2: record_index (dict)
        param3: mode (str)

    """
    if mode == 'mark' and record_index['in_range']:
        matrix.todo_quarters[user_input].todo_items[record_index['index']].mark()

    elif mode == 'unmark' and record_index['in_range']:
        matrix.todo_quarters[user_input].todo_items[record_index['index']].unmark()

    sleep(0.625)


def toggle_mark_mode(pressed_key, matrix, user_input, records_amount, working_mode):
    """
    Depends on the user input, this function allows selecting between
    mark task and unmark task which means done or undone.

    Args:
        param1: pressed_key (int)
        param2: matrix (TodoMatrix object)
        param3: user_input (int)
        param4: records_amount (int) amount of tasks in quarter
        param5: working_mode (bool)

    Return:
        working_mode (bool)

    """
    if pressed_key == '1':
        record_index = is_index_in_range(matrix, records_amount)
        toggle_mark(matrix, record_index, user_input, 'mark')

    elif pressed_key == '2':
        record_index = is_index_in_range(matrix, records_amount)
        toggle_mark(matrix, record_index, user_input, 'unmark')

    elif pressed_key == '0':
        working_mode = False

    return working_mode


def toggle_mark_mode_specification():
    menu = ['Mark Task', 'Unmark Task']
    title = 'Toggle mark mode:'

    return menu, title


def remove_item(pressed_key, matrix, user_input, records_amount, working_mode):
    """
    This function remove object from quarter

    Args:
        param1: pressed_key (int)
        param2: matrix (TodoMatrix object)
        param3: user_input (int)
        param4: records_amount (int) amount of tasks in quarter
        param5: working_mode (bool)

    Return:
        working_mode (bool)

    """
    records_list = matrix.todo_quarters[user_input].todo_items

    if pressed_key == '1':
        record_index = is_index_in_range(matrix, records_amount)
        if record_index['in_range'] and records_list:
            del records_list[record_index['index']]

        else:
            ui.print_error_message('Out of range or no item in this quarter.')
            sleep(1)

    elif pressed_key == '0':
        working_mode = False

    return working_mode


def remove_mode_specification():
    menu = ['Delete record']
    title = 'Record manager:'

    return menu, title


def universal_body(matrix, mode):
    """
    This function body support multiple actions from menu.

    Args:
        param1: matrix (TodoMatrix object)
        param2: mode (str) order to do

    """
    user_input = get_quarter_status(matrix, True)
    working = True
    records_amount = len(matrix.get_quarter(user_input).todo_items)

    if mode == 'mark_mode':
        menu, title = toggle_mark_mode_specification()

    elif mode == 'remove_mode':
        menu, title = remove_mode_specification()

    if records_amount > 0:
        while working:
            os.system("clear")
            show_items(matrix, user_input)
            ui.print_menu(title, menu, 'Exit', True)
            pressed_key = ui.get_inputs(['Your choice'])[0]

            if mode == 'mark_mode':
                working = toggle_mark_mode(pressed_key, matrix, user_input, records_amount, working)

            elif mode == 'remove_mode':
                working = remove_item(pressed_key, matrix, user_input, records_amount, working)

    else:
        show_items(matrix, user_input)


def archive_items(matrix):
    # deleting tasks which are marked as done
    matrix.archive_items()


















    #
