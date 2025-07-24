# Honeybadger

Honeybadger is a Python-based bot designed to provide Formula 1 data and alerts. It leverages the FastF1 library to fetch and process F1 data, and includes commands for standings, race schedules, and more.

## Project Structure

- `bot.py` - Main entry point for the bot.
- `keep_alive.py` - Keeps the bot running (useful for hosting on platforms like Replit).
- `requirements.txt` - Python dependencies for the project.
- `commands/` - Contains command modules for the bot (e.g., driver standings, constructor standings, next race info).
- `tasks/` - Scheduled or background tasks (e.g., alerts).
- `fastf1_data/` - Directory for FastF1 data cache or related files.
- `utils/` - Utility functions and helpers (if any).

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/N0Xl0US/honeybadger
   cd honeybadger
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the bot:**
   ```bash
   python bot.py
   ```

## Features
- Get current driver and constructor standings
- Find out when the next race is
- Receive F1 alerts (see `tasks/alerts.py`)

## Requirements
- Python 3.8+
- See `requirements.txt` for Python package dependencies

## Contributing
Pull requests and issues are welcome! Please open an issue to discuss your ideas or report bugs.

## License
[MIT](LICENSE)
