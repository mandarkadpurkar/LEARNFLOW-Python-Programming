import requests

def get_exchange_rates(base_currency):
    # Replace 'API_KEY' with your actual API key from https://exchangeratesapi.io/
    api_key = 'API_KEY' #Original key has been removed because it is associated with billing account
    
    # Construct the API URL for fetching exchange rates for the specified base currency
    url = f'https://open.er-api.com/v6/latest/{base_currency}?apiKey={api_key}'
    
    # Make a GET request to the API
    response = requests.get(url)
    data = response.json()
    
    # Check if the API request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Return the exchange rates as a dictionary
        return data['rates']
    else:
        # Raise an exception if the API request was not successful
        raise Exception(f"Failed to fetch exchange rates: {data['error']['info']}")

def convert_currency(amount, from_currency, to_currency):
    # Get the latest exchange rates for the source currency
    exchange_rates = get_exchange_rates(from_currency)
    
    # Check if the target currency is valid
    if to_currency not in exchange_rates:
        raise ValueError(f"Invalid target currency: {to_currency}")
    
    # Retrieve the conversion rate for the target currency
    conversion_rate = exchange_rates[to_currency]
    
    # Perform the currency conversion
    converted_amount = amount * conversion_rate
    
    # Return the converted amount
    return converted_amount

def main():
    try:
        # Get user input for the amount, source currency, and target currency
        amount = float(input("Enter the amount: "))
        from_currency = input("Enter the source currency code: ").upper()
        to_currency = input("Enter the target currency code: ").upper()
        
        # Perform the currency conversion
        converted_amount = convert_currency(amount, from_currency, to_currency)
        
        # Display the result to the user
        print(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}")
    
    except ValueError as e:
        # Handle input conversion errors
        print(f"Error: {e}")
    
if __name__ == "__main__":
    # Run the main function when the script is executed
    main()
