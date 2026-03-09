# config/sites.py
"""
Central registry of supported sites.

Each key is a short alias used with the --site CLI flag.
The value is the base URL for that site.
"""

SITES: dict[str, str] = {
    "internet": "https://the-internet.herokuapp.com",
    "saucedemo": "https://www.saucedemo.com",
    "demoqa": "https://demoqa.com",
}
