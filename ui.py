import os


def get_inputs(labels):
    """
    Get input from user

    Args:
        param1: labels (list)

    return:
        temp (list of provided values)

    """
    temp = []

    for question in labels:
        ask = input(question+': ')
        temp.append(ask)

    return temp


def print_menu(title, labels, exit_message, enumerate_options=True):
    """
    Args:
        param1: title (string)
        param2: labels (list)
        param3: exit_message (string)
        param4: enumerate_options (bool)
    """
    print('\n' + title)

    for i in range(len(labels)):
        if enumerate_options:
            print('{}({}) {}'.format('\t', str(i+1), labels[i]))
        else:
            print('{} {}'.format('\t', labels[i]))

    if exit_message:
        print('{}({}) {}\n'.format('\t', '0', exit_message))


def print_error_message(message):
    """
    This function just print to output stream a message

    Args:
        param1: message (string)
    """
    print(message)


def print_result(result, mode):

    if mode == 'get_quarter':
        print(result)
