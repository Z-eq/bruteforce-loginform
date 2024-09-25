# Login Form Finder for Brute-Force Attacks

This Python script is designed to locate login forms on web pages for the purpose of performing brute-force attacks. Instead of using tools like Burp Suite, this script identifies login forms and generates the necessary command for tools like Hydra for password cracking.

## Features

- Automatically retrieves web pages to identify forms.
- Analyzes HTML to find login fields (username and password).
- Generates Hydra commands for brute-force attacks based on identified fields.
- Supports both automatic and manual login attempts for testing.

## Usage

1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install requests beautifulsoup4 urllib3


## Requirements

- Python 3.x
- `requests` library
- `BeautifulSoup` (from `bs4`)
- `urllib3`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Z-eq/bruteforce-loginform/brute-form.git

