import ui
import eisenhower_matrix


def choose():
    user_input = ui.get_inputs(['What do you want to do'])

    if user_input == ['1']:
        eisenhower_matrix.start_module()

    elif user_input == ['0']:
        exit()

    else:
        ui.print_error_message("\033[1;31m" + 'This option does not exist.' + "\033[0;0m")


def handle_menu():
    possible_option = ['Eisenhower Matrix']
    ui.print_menu('Main menu:', possible_option, 'Exit')


def main():

    while True:
        handle_menu()
        choose()


if __name__ == '__main__':
    main()
