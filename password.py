import argparse
import base64
import sys


def decode(password):
    if password == "cXdlcnR5":
        result = base64.b64decode(password)
        print(f'\nInnocent until proven guilty, they key is: "{result.decode()}"')
    else:
        print("Uh Uh Uh, You haven't said the magic word!!!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Decodes Base64 passwords for you to have the keys to the kingdom!!!!, Coded by Elliot Alderson.")

    parser.add_argument("-p", "--password", help="Password intended to be decoded", required=True)

    args = parser.parse_args()
    if len(sys.argv[1:]) == 0:
        parser.print_usage()

    if args.password:
        decode(args.password)
