if __name__ == "__main__":
    print(f'initializing OutQuantLab...')
    from sys import exit
    from App import OutQuantLabCLI, OutQuantLabGUI
    def launch_choice(choice: int) -> None:
        if choice == 1:
            OutQuantLabCLI()
            exit(0)
        else:
            app = OutQuantLabGUI()
            exit(app.exec())
    
    launch_choice(choice=2)