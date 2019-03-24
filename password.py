import argparse
import base64


def decode(password):
    if password == "cXdlcnR5":
        result = base64.b64decode(password)
        print(f'Your decoded password is "{result.decode()}"')
    else:
        print("Uh Uh Uh, You haven't said the magic word!!!")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Decodes Base64 for passwords for you the keys to the kingdom, Coded by Elliot Alderson.")

    parser.add_argument("-p", "--password", help="Password intended to be decoded")

    args = parser.parse_args()
    decode(args.password)
