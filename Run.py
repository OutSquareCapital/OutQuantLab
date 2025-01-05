if __name__ == "__main__":
    print(f'initializing OutQuantLab...')
    from sys import exit
    from App import OutQuantLabCLI, OutQuantLabGUI
    def launch_choice(choice: str) -> None:
        if choice == '1':
            OutQuantLabCLI()
            exit(0)
        elif choice == '2':
            app = OutQuantLabGUI()
            exit(app.exec())
        else:
            print("Exiting...")
            exit(0)
    #choice = input("Enter 1 to run CLI, 2 to run GUI: ")
    launch_choice(choice='1')