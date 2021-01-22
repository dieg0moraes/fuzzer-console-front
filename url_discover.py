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
        init(autoreset=True)

        print(Fore.CYAN + "Setup...\n")

        save = query_yes_no("Do you want to save results ?", default="no")
        self.fuzzer = Fuzzer(save=save)

        self.logger = self.fuzzer.logger

        print("Select the dictionary to use")

        self.dictionary = self.get_dictionary()

        self.url = input("Write the url to use: ")

        self.dictionary = ""
        self.url = ""
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
        if not filename:
            print(Fore.LIGHTRED_EX + "Canceled. Aborting...")
            sleep(1)
            sysexit(0)
        return filename


    def settings(self):
        """Change settings"""
        while True:
            console.clear()
            # Cannot use Tor and a proxy at the same time.
            if self.tor:
                proxy_option = Fore.LIGHTBLACK_EX + "[4] Proxy" + Fore.RESET
            else:
                proxy_option = f"[4] Proxy --> {self.proxy}"
            
            if self.end == END_DEFAULT:
                end_option = Fore.CYAN + "LAST WORD" + Fore.RESET
            else:
                end_option = self.end

            print(f"""
            [1] Workers --> {self.workers}
            [2] Timeout --> {self.timeout}
            [3] Tor --> {self.tor}
            {proxy_option}
            [5] Start word --> {self.start}
            [6] End word --> {end_option}
            [7] Intervals --> {self.interval}

            [99] Return
            """)
            option = input("--> ")

            # If the option is an int:
            if not option in ("3", "4"):
                new_value = int(input("New value: "))
                if (new_value < 1 and option != "5") or new_value < 0:
                    self.logger.lerr("Invalid value given")
                    continue

                if option == "1":
                    self.workers = new_value

                elif option == "2":
                    self.timeout = new_value

                elif option == "5":
                    if new_value >= self.end:
                        self.logger.lerr("Start must be smaller than end")
                        continue
                    self.start = new_value

                elif option == "6":
                    if new_value <= self.start:
                        self.logger.lerr("End must be grater than start")
                        continue
                    self.end = new_value

                elif option == "7":
                    self.interval = new_value

            elif option == "3":
                self.tor = not self.tor

            elif option == "4":
                if self.tor:
                    print(Fore.RED + "Disable Tor to use a custom proxy!")
                    continue
                self.proxy = input("Proxy to use: ")

            elif option == "99":
                break

            else:
                self.logger.lerr("Try again.")
                sleep(2)


    def main(self):
        while True:
            console.banner("Url Discovery Module")
            # TODO: Print options.
            try:
                self.settings()
            except ValueError:
                self.logger.lerr("Value error!")
                sleep(1)
