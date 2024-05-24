"""
    Author: Kyle Lamont | @Zero2164
    Authored by 2024
    Date Created: 21/05/2024 
    Date Last Modified: 22/05/2024 
"""

# --- MODULES --- #
import requests, os, sys, argparse

# --- VARIABLES --- #

# Current Token for FreeCurrencyAPI
CURR_TOKEN = os.getenv("CURR_TOKEN")
assert CURR_TOKEN is not None, "CURR_TOKEN is not set"

# Base URL for the FreeCurrencyAPI
BASE_URL = f"https://api.freecurrencyapi.com/v1/latest?apikey={CURR_TOKEN}"

# Currencies List
CURRENCIES = ["USD", "EUR", "AUD", "CAD", "GBP", "JPY", "CNY", "INR", "KRW"]

# Mapping of currency codes to icons
CURRENCY_ICONS = {
    "USD": "$",
    "EUR": "€",
    "AUD": "A$",
    "CAD": "C$",
    "GBP": "£",
    "JPY": "¥",
    "CNY": "¥",
    "INR": "₹",
    "KRW": "₩",
}


# --- FUNCTIONS --- #

# Argument Parser Function
parser = argparse.ArgumentParser(
    description=f"""
    Description:\n\nMass-Fetches the latest currency exchange rates for a given base currency as well as optionally converts and displays a base currency value next to each result.
    CURRENCIES list: {CURRENCIES}
    """
)

parser.add_argument(
    "base_currency[str]",
    type=str,
    nargs="?",
    help="""Enter the base currency (USD, EUR, AUD, CAD, etc.) - See CURRENCIES List in Description.""",
)
parser.add_argument(
    "base_value[float]",
    type=float,
    nargs="?",
    help="(Optional) Enter the base currency value to be converted.",
)

args = parser.parse_args()


# Currency Converter Function
def convert_currency(base):

    currencies = ",".join(CURRENCIES)
    url = f"{BASE_URL}&base_currency={base}&currencies={currencies}"
    try:
        response = requests.get(url)
        data = response.json()
        return data["data"]
    except Exception as e:
        print(
            "Error fetching currency exchange rates. Please try again later.\nException message is {e}\n"
        )
        return None


# --- Main Function --- #
def __main__():
    while True:
        # Handle input
        if len(sys.argv) > 1:
            base = sys.argv[1]
        else:
            base = (
                input(
                    "\nEnter the base currency (USD, EUR, AUD, CAD, etc. or q to quit): "
                ).upper()
                or "AUD"
            )

        if base == "Q":
            print("\nBye!")
            break

        if base not in CURRENCIES:
            print("\nInvalid option. Please try again.\n")
            continue

        value = ""
        skip = False
        if len(sys.argv) > 2:
            value = sys.argv[2]
        else:
            value = input(
                "\nEnter the currency value (0 to skip or q to quit): "
            ).upper()

        if value == "Q":
            print("\nBye!")
            break

        if value != "0" and type(value) == str:
            # test if value is a number
            try:
                value = float(value)
            except ValueError:
                print("\nInvalid currency value or option entered. Please try again.\n")
                continue
        else:
            skip = True
            print("No currency value entered. Skipping conversion...\n")

        # Get the base currency
        data = convert_currency(base)
        if not data:
            continue

        # OUTPUT - Display the exchange rates
        print("\n================================================")
        if not skip:
            print(
                f"({base}) currency valued at {CURRENCY_ICONS[base]} {value} coverts to:\n"
            )
        else:
            print(
                f"({base}) currency valued at {CURRENCY_ICONS[base]} {data[base]} coverts to:\n"
            )
        del data[base]
        for curr, rate in data.items():
            if not skip:
                rate = float(rate) * value
            print(f"    ({curr}) {CURRENCY_ICONS[curr]} {round(rate, 2)}")
        print("================================================")
        print("\nWant to convert another currency?")

        # Reset sys.argv
        sys.argv = sys.argv[:1]


__main__()
