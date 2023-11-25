import requests

class CurrencyConverter:

    def __init__(self):
        self.rates = {}

    def get_rates(self):
        response = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")
        data = response.json()
        for item in data:
            self.rates[item['cc']] = item['rate']

    def convert(self, amount, from_currency, to_currency):
        try:
            if from_currency != "USD":
                amount = amount / self.rates[from_currency]
            converted_amount = round(amount * self.rates[to_currency.upper()], 2)
            return converted_amount
        except KeyError:
            raise KeyError(f"Invalid currency code entered: {from_currency} or {to_currency}")
        except ZeroDivisionError:
            raise ValueError("Cannot convert from USD to USD.")
        except Exception as e:
            raise e

converter = CurrencyConverter()

try:
    converter.get_rates()

    while True:
        try:
            amount = float(input("Enter the amount of currency: "))
            from_currency = input("Enter the currency code of the amount you entered: ")
            to_currency = "USD"

            
            if from_currency.upper() not in converter.rates:
                raise KeyError(f"Invalid currency code entered: {from_currency}")

            converted_amount = converter.convert(amount, from_currency.upper(), to_currency)

            print("The amount of {} {} is equal to {:.2f} USD".format(amount, from_currency.upper(), converted_amount))
            break

        except (KeyError, ValueError) as e:
            print(e)


except requests.RequestException as e:
    print(f"Error fetching exchange rates: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
