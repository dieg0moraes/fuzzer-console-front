"""
Copyright (c) 2021 Diego Moraes. MIT license, see LICENSE file.
"""
import console
from cli import main
from time import sleep
from sys import exit as sysexit


def fuzzer_credits():
    print("@-------------------------------------------------------@")
    print("| Creator: Diego Moraes (https://github.com/dieg0moraes)|")
    print("| Contributor: Nanush7 (https://github.com/Nanush7)     |")
    print("@-------------------------------------------------------@")


def fuzzer_license():
    with open("LICENSE", "r") as license_file:
        license_text = license_file.read()
        print(license_text)


while True:
    console.banner("Fuzzer framework")
    print("""

    [1] Start
    [2] Credits
    [3] License

    [99] Exit
    """)

    option = input("--> ")

    if option == "1":
        main()
    elif option == "2":
        fuzzer_credits()
    elif option == "3":
        fuzzer_license()
    elif option == "99":
        sysexit(0)
    else:
        print("Invalid option. Try again")
        sleep(2)
        continue
    input("Press Enter to continue...")
