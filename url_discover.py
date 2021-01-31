"""
Copyright (c) 2021 Diego Moraes. MIT license, see LICENSE file.
"""
import console
from time import sleep
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from colorama import init, Fore
from logic.fuzzer import Fuzzer
from logic.settings import WORKERS, TIMEOUT, END_DEFAULT
from utils import query_yes_no
from sys import exit as sysexit


class UrlDiscover:
    def __init__(self):
        console.banner("Url Discovery Module Setup")

        init(autoreset=True)

        save = query_yes_no("Do you want to save results ?", default="no")
        self.fuzzer = Fuzzer(save=save)

        self.logger = self.fuzzer.logger

        print("Select the dictionary to use")

        self.dictionary = self.get_dictionary()
        if not self.dictionary:
            self.log_error("Canceled. Aborting...")
            sysexit(0)

        self.url = input("Write the url to use: ")

        self.workers = WORKERS
        self.timeout = TIMEOUT
        self.tor = False
        self.proxy = None
        self.start = 0
        self.end = END_DEFAULT
        self.interval = 0


    def get_dictionary(self):
        """Get dictionary file"""
        Tk().withdraw()
        self.logger.linfo("Waiting for dictionary selection...")
        filename = askopenfilename()
        return filename


    def log_error(self, message):
        """Log error and wait to clear screen"""
        self.logger.lerr(message)
        sleep(2)


    def settings(self):
        """Change settings"""
        while True:
            console.clear()
            # Disable Proxy option if Tor is in use #
            if self.tor:
                proxy_option = Fore.LIGHTBLACK_EX + "Proxy" + Fore.RESET
            else:
                proxy_option = f"Proxy --> {self.proxy}"

            if self.end == END_DEFAULT:
                end_option = Fore.CYAN + "LAST WORD" + Fore.RESET
            else:
                end_option = self.end

            # Display options #
            print(f"""
            [1] Workers --> {self.workers}
            [2] Timeout --> {self.timeout}
            [3] Tor --> {self.tor}
            [4] {proxy_option}
            [5] Start word --> {self.start}
            [6] End word --> {end_option}
            [7] Intervals --> {self.interval}

            [99] Return
            """)
            option = input("--> ")

            # Validate and set #

            # Tor
            if option == "3":
                self.tor = not self.tor

            # Proxy
            elif option == "4":
                if self.tor:
                    self.log_error("Disable Tor to use a custom proxy!")
                    continue
                print("Leave blank to disable proxy.")
                self.proxy = input("Proxy to use: ")
                if self.proxy == "":
                    self.proxy = None

            # Workers
            elif option == "1":
                new_value = int(input("Number of workers = "))
                if new_value < 1:
                    self.log_error("Must be grater than 1.")
                    continue
                self.workers = new_value

            # Timeout
            elif option == "2":
                new_value = int(input("Timeout in seconds = "))
                if new_value < 1:
                    self.log_error("Must be grater than 1.")
                    continue
                self.timeout = new_value

            # Start word
            elif option == "5":
                new_value = int(input("First word index = "))
                if new_value >= self.end and self.end != END_DEFAULT:
                    self.log_error("Start must be smaller than end")
                    continue
                if new_value < 0:
                    self.log_error("Must be a positive number.")
                    continue
                self.start = new_value

            # End word
            elif option == "6":
                print(f"Set this to {END_DEFAULT} to use the last word of the dictionary")
                new_value = int(input("Last word index = "))
                if new_value != END_DEFAULT and new_value <= self.start:
                    self.log_error("End must be grater than start")
                    continue
                self.end = new_value

            # Intervals
            elif option == "7":
                new_value = int(input("Requests per interval = "))
                if new_value < 0:
                    self.log_error("Must be a positive number.")
                    continue
                self.interval = new_value

            # Exit
            elif option == "99":
                break

            else:
                self.log_error("Try again.")


    def run(self):
        """Start execution"""
        self.fuzzer.timeout = self.timeout
        self.fuzzer.workers = self.workers
        self.fuzzer.tor = self.tor
        self.fuzzer.proxy = self.proxy
        self.fuzzer.set_target(self.dictionary, self.url, self.start, self.end)
        self.fuzzer.build_urls(ask=True)
        self.fuzzer.run(self.interval)
        self.fuzzer.print_stats()

        console.cont()


    def main(self):
        while True:
            console.banner("Url Discovery Module")

            print(f"""
            [1] Run fuzzer
            [2] Change settings
            [3] Url: {self.url}
            [4] Dictionary: {self.dictionary}
            [99] Return
            """)
            option = input("--> ")
            if option == "1":
                self.run()

            elif option == "2":
                try:
                    self.settings()
                except ValueError:
                    self.logger.lerr("Value error!")
                    sleep(1)

            elif option == "3":
                self.url = input("New url: ")

            elif option == "4":
                filename = self.get_dictionary()
                if filename:
                    self.dictionary = filename

            elif option == "99":
                break
