# Telegram Language Bot 🐈

<p align="center">
  <img src="./cat_avatar.jpg" alt="Bot Avatar" width="250">
</p>

Telegram bot that checks message scripts and warns users when they use unsupported languages.

## Supported Languages

* English 🏴󠁧󠁢󠁥󠁮󠁧󠁿
* Georgian 🇬🇪

## Detection Rules

The bot allows:

* ASCII English letters: `A-Z`, `a-z`
* Georgian letters
* Numbers, punctuation, emoji, and other non-letter characters

The bot warns when a message contains any other Unicode letter. This includes:

* Non-Latin scripts, such as Cyrillic, Armenian, Hebrew, or Arabic
* Extended Latin letters with accents or language-specific marks, such as `ñ`, `ç`, `ł`, `ß`, `ø`, or `đ`

Examples that trigger a warning:

```text
Hayırlı akşamlar
schöne Grüße
Cześć
Hola, niños!
Xin chào
Привет
שלום
```

Examples that do not trigger a warning:

```text
Hello
Price: 5 lari
გამარჯობა
😬😬😬
```

This is still a script and character check, not full language detection. Unsupported languages written only with plain ASCII letters, such as `Guten Abend`, `Dzien dobry`, or `Merhaba`, can look the same as English-style text to this bot.

## Technologies

* Python 3.12+
* python-telegram-bot
* python-dotenv
* Docker
* Docker Compose

---

## Project Structure

```text
.
├── bot.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

---

## Local Development

### Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Dev: Freeze Dependencies

```bash
pip freeze > requirements.txt
```

### Run Tests

```bash
python3 -m unittest discover -s tests
```

### Configure Environment Variables

Create a `.env` file:

```env
BOT_TOKEN=your_telegram_bot_token
```

### Run Locally

```bash
python bot.py
```

---

## Docker

### Build Image

```bash
docker build -t telegram-language-bot .
```

The Docker build runs the unit tests and fails if any test fails.

### Run Container

```bash
docker run --env-file .env telegram-language-bot
```

---

## Docker Compose

### Start

```bash
docker compose up --build
```

### Start in Background

```bash
docker compose up -d --build
```

### View Logs

```bash
docker compose logs -f
```

### Stop

```bash
docker compose down
```

---

## Create Telegram Bot

1. Open Telegram.
2. Find `@BotFather`.
3. Run:

```text
/newbot
```

4. Copy the generated bot token.
5. Put it into the `.env` file.

### Set Bot Avatar

```text
/setuserpic
```

### Change Description

```text
/setdescription
```

### Change About Text

```text
/setabouttext
```

---

## Group Usage

To monitor all messages in a group:

1. Add the bot to the group.
2. Open BotFather.
3. Disable privacy mode:

```text
/mybots
→ Select bot
→ Bot Settings
→ Group Privacy
→ Turn Off
```

Without this setting the bot will not receive all group messages.

---

## Deploy to Oracle Cloud Always Free

### Create VM

Recommended configuration:

* Ubuntu 22.04 or 24.04
* Ampere A1 (Always Free)
* 1 OCPU
* 6 GB RAM

### Connect

```bash
ssh -i ~/.ssh/oracle_ssh.key ubuntu@SERVER_IP
```

### Install Docker

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2 git
```

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/telegram-language-bot.git
cd telegram-language-bot
```

### Create Environment File

```bash
nano .env
```

```env
BOT_TOKEN=your_telegram_bot_token
```

### Start Bot

```bash
docker compose up -d --build
```

### Check Status

```bash
docker ps
```

### View Logs

```bash
docker compose logs -f
```

### Update Application

```bash
git pull --rebase
docker compose up -d --build
```

---

## Notes

* The bot uses Telegram polling (`run_polling()`).
* No inbound ports need to be opened.
* Docker automatically restarts the container after server reboot (`restart: unless-stopped`).

---

## Future Improvements

* Delete unsupported messages automatically
* Warn users only once
* Configure allowed languages via environment variables
* Admin whitelist
* Language usage statistics
* AI-powered language detection
* Support multiple Telegram groups
