# Burger Stop

8-bit burger shop game. Read the ticket, stack ingredients in order, then serve.

How the code is structured: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Setup

Use Python 3.10 or newer. The game depends on **pygame-ce** (Community Edition), not classic pygame.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Windows

1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/). During setup, check **Add python.exe to PATH**.
2. Open **Command Prompt** or **PowerShell** in the `burger-stop` folder.
3. Create a virtual environment, install dependencies, and run:

```bat
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

If `py` is not recognized, use `python` in place of `py -3`.

To leave the virtual environment later, run `deactivate`.

## Play

- Click ingredients on the right to stack them. Tray is stacked like a burger (top bun at the top).
- Click a layer on the burger to pull that ingredient out.
- **SERVE** checks the stack against the ticket.
- **CLEAR** dumps the current stack.
- Each order has **30 seconds**. The customer gets madder as the clock runs down.
- If time runs out they curse, storm off (**-2**), and the next customer arrives.
- Correct order: burger flashes green, **+10** score, next customer.
- Wrong order: burger flashes red, **-2** score (not below 0), try again.

Pixel typeface: [Press Start 2P](https://github.com/google/fonts/tree/main/ofl/pressstart2p) (SIL Open Font License).
