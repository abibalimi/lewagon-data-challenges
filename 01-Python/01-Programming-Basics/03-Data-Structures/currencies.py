# pylint: disable=missing-docstring

# TODO: add some currency rates # pylint: disable=fixme
RATES = {"USDEUR": 0.85, "GBPEUR": 1.13, "CHFEUR": 0.86, "EURGBP": 0.885}

def convert(amount, currency):
    """returns the converted amount in the given currency
    amount is a tuple like (100, "EUR")
    currency is a string
    """
    if amount[1]+currency not in RATES:
        result = None
    elif amount[1] == "USD" and currency == 'EUR':
        result = round(amount[0] * RATES["USDEUR"])
    elif amount[1] == "GBP" and currency == 'EUR':
        result = round(amount[0] * RATES["GBPEUR"])
    elif amount[1] == "CHF" and currency == 'EUR':
        result = round(amount[0] * RATES["CHFEUR"])
    elif amount[1] == "EUR" and currency == 'GBP':
        result = round(amount[0] * RATES["EURGBP"])
    return result
