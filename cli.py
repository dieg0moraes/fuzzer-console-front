"""
Copyright (c) 2021 Diego Moraes. MIT license, see LICENSE file.
"""
import console
from time import sleep
from url_discover import UrlDiscover


def home():
    """Main Menu"""
    print("""
    [1] Url discovery
    [2] Payload fuzzing

    [99] Return
    """)
    option = input("--> ")
    return option


def main():
    # Start
    while True:
        console.banner("Fuzzing script")
        option = home()
        if option == "1":
            fuzzer = UrlDiscover()
            fuzzer.main()
        elif option == "2":
            raise NotImplementedError
        elif option == "99":
            break
        else:
            print("Try again.")
            sleep(2)


if __name__ == "__main__":
    main()
