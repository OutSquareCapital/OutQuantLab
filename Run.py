def launch_choice(choice: int) -> None:
    if choice == 1:
        OutQuantLabCLI()
        exit(0)
    else:
        app = OutQuantLabGUI()
        exit(app.exec())

if __name__ == "__main__":

    print('initializing OutQuantLab...')

    from sys import exit
    from App import OutQuantLabCLI, OutQuantLabGUI

    launch_choice(choice=1)