import requests


API_KEY = "b91a78f76c616d979b77f713"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

def get_exchange_rate(base_currency, target_currency):
    """Fetches exchange rate from base_currency to target_currency."""
    response = requests.get(BASE_URL + base_currency)
    data = response.json()

    if response.status_code != 200:
        print("Error fetching exchange rates:", data["error-type"])
        return None

    rates = data.get("conversion_rates", {})
    return rates.get(target_currency)

def convert_currency():
    """Handles user input and performs currency conversion."""
    print("\n== Welcome to the MeMe Currency Converter CLI! ==")
    print("----------------------------------------------------\n")
    
    base_currency = input("Enter the base currency (e.g., USD): ").upper()
    target_currency = input("Enter the target currency (e.g., EUR): ").upper()
    amount = float(input(f"Enter amount in {base_currency}: "))

    exchange_rate = get_exchange_rate(base_currency, target_currency)

    if exchange_rate:
        converted_amount = amount * exchange_rate
        print(f"\n✅ {amount} {base_currency} = {converted_amount:.2f} {target_currency}\n")
    else:
        print("\n❌ Invalid currency or API error. Please try again.")

if __name__ == "__main__":
    choice = True
    convert_currency()
    while choice:
        user_input = input("Do you want to continue? (y/n) ").casefold()
        if user_input == 'y':
            convert_currency()
        else:
            print("== Thank you for using MeMe currency converter ==")
            break
        
