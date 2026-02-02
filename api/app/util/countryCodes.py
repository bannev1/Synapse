COUNTRY_CODES = {
	'us': 'United States',
	'uk': 'United Kingdom',
	'cn': 'China',
	'ca': 'Canada',
	'ge': 'Germany'
}


def convertCodeToCountry(code: str) -> str:
	"""
	Given a country code convert it to its country name equivalent
	"""

	try:
		return COUNTRY_CODES[code]
	except IndexError:
		return '' # If doesn't correspond


def convertCountryToCode(country: str) -> str:
	"""
	Given a country name convert it to its country code equivalent
	"""

	flipped = {code: country for country, code in COUNTRY_CODES.items()}

	try:
		return flipped[country]
	except IndexError:
		return '' # If doesn't correspond
