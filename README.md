# Poker Bot

This is a poker bot designed for automatic play in online poker rooms. It uses Selenium and other libraries to interact with web pages, simulate poker games, and make decisions based on calculated probabilities.

## Features

- **Automatic Poker Play**: The bot interacts with poker tables, places bets, and performs actions based on a set of rules and calculations.
- **Card and Board Detection**: It identifies cards in the player's hand, the community cards (board), and calculates the probabilities of winning.
- **Simulation-based Decision Making**: The bot uses poker hand simulation results to decide its actions (e.g., fold, raise, call).
- **Dynamic Table Interaction**: It joins different poker tables, waits for spots, and handles various poker actions automatically.
- **Risk and Sensitivity Control**: The bot allows you to adjust the risk sensitivity to make more conservative or more aggressive plays.

## Installation

### Requirements

- Python 3.6 or higher
- Chrome WebDriver (Automatically handled by `chromedriver-autoinstaller`)
- `undetected_chromedriver` (to bypass detection of bots)
- Selenium
- Other dependencies specified in `requirements.txt`

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/poker-bot.git
   cd poker-bot
   ```

2. **Install Dependencies**

   You can install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, install the individual dependencies:

   ```bash
   pip install selenium undetected_chromedriver chromedriver-autoinstaller
   ```

3. **Set Up Chrome WebDriver**

   The bot automatically installs the necessary Chrome WebDriver using `chromedriver-autoinstaller`, so there's no need to manually download it.

4. **Run the Bot**

   To start the bot, run the main Python script:

   ```bash
   python poker_bot.py
   ```

## Usage

### Main Workflow

1. **Login**: The bot will log in to the specified poker room using the credentials set in the script.
2. **Join Rooms**: It searches for available poker tables and attempts to join one with the appropriate number of players and blind values.
3. **Gameplay**: The bot will automatically interact with the table by:
   - Detecting its own hand and the community cards (flop, turn, river).
   - Calculating the probability of winning based on simulations or predefined results.
   - Deciding whether to fold, raise, or call based on calculated pot odds, hand strength, and risk tolerance.
4. **Timeout Handling**: If no action is needed or if certain conditions are met (such as reaching the maximum play time), the bot will exit the room and attempt to find a new table or quit entirely.
5. **Risk Sensitivity**: The bot's behavior can be adjusted using the `risk_value` parameter. A value closer to 1 will make the bot take higher risks, while a lower value will make it more conservative.

### Parameters

- **`risk_value`**: Controls how risky the bot plays. A higher value means higher risk (more aggressive actions), and a lower value makes the bot play more cautiously.

### Examples of Hands

The bot has predefined "strong hands" such as:

- **Strong Hands**: Pairs, high-ranking suited cards (e.g., `As Ah`, `Ks Kd`).
- **Strong Hands Plus**: Even stronger hands with some variations.

These hands are used in simulations to calculate the bot's odds and decide its actions.

### Error Handling

- The bot handles errors like connection issues and login failures, and it will attempt to reconnect if needed.
- It also manages table actions, like leaving the table or confirming a fold, and retries if it fails to perform an action.

## Simulations

The bot uses its own poker simulator (e.g., `simulator3.py`) to calculate hand probabilities. These simulations are based on the number of players at the table and the community cards that have been dealt.

## Files

- **`poker_bot.py`**: Main script to run the poker bot.
- **`simulator3.py`**: Contains the poker hand simulator for calculating win probabilities.
- **`new_results_simulation.json`**: Predefined simulation results used by the bot for decision-making.
- **`requirements.txt`**: List of Python dependencies.

## Contributing

If you'd like to contribute to this project, feel free to fork it and submit a pull request. Issues and bug reports are also welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This bot is intended for educational purposes only. Use it at your own risk. The author is not responsible for any consequences of its usage in real-world poker games or casinos.
```

This README covers the key points about setting up, using, and understanding the poker bot script. Modify and adapt it as necessary based on the actual functionality and the specific details of your project.
