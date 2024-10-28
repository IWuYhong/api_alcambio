import requests

# API endpoint URL
url = "https://api.alcambio.app/graphql"

# Function to execute the GraphQL query
def get_conversion_rates():
  """
  Executes the GraphQL query to fetch conversion rates for a country.

  Returns:
      A dictionary containing the conversion rates or None on error.
  """
  query = """
query {
  getCountryConversions(payload: {countryCode: "VE"}) {
    _id
    baseCurrency {
      code
      decimalDigits
      name
      rounding
      symbol
      symbolNative
    }
    country {
      code
      dial_code
      flag
      name
    }
    conversionRates {
      baseValue
      official
      principal
      usesRateValue
      rateCurrency {
        code
        decimalDigits
        name
        rounding
        symbol
        symbolNative
      }
      rateValue
      type
    }
    dateBcvFees
    dateParalelo
    dateBcv
    createdAt
  }
}
  """

  # Send POST request with JSON data
  response = requests.post(url, json={"query": query})

  # Check for successful response
  if response.status_code == 200:
    data = response.json().get("data")
    if data:
      return data.get("getCountryConversions")
    else:
      print("Error: No data found in response.")
  else:
    print("Error:", response.status_code, response.text)
  return None

conversion_data = get_conversion_rates()

if conversion_data:
  # Extract base currency code
  base_currency_code = conversion_data.get("country").get("name")

  # Print conversion rates for each requested currency
  print(f"\nConversion Rates for ({base_currency_code}):")
  for rate in conversion_data.get("conversionRates"):
    if rate['official'] == True:
        rate_currency_code = rate.get("rateCurrency").get("code")
        rate_symbol = rate.get("rateCurrency").get("symbol")
        rate_value = rate.get("baseValue")
        print(f"{rate_currency_code} Official ({rate_symbol}): Bs.S {rate_value} ")
    else:
        rate_currency_code = rate.get("rateCurrency").get("code")
        rate_symbol = rate.get("rateCurrency").get("symbol")
        rate_value = rate.get("baseValue")
        print(f"{rate_currency_code} No Oficial ({rate_symbol}): Bs.S {rate_value} ")
else:
  print("Error: Failed to retrieve conversion rates.")
