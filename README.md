# Burger Stop

8-bit burger shop game. Read the ticket, stack ingredients in order, then serve.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Play

- Click ingredients on the right to stack them.
- **SERVE** checks the stack against the ticket.
- **CLEAR** dumps the current stack.
- Correct order: burger flashes green, **+10** score, next customer.
- Wrong order: burger flashes red, **-2** score (not below 0), try again.

Pixel typeface: [Press Start 2P](https://github.com/google/fonts/tree/main/ofl/pressstart2p) (SIL Open Font License).
