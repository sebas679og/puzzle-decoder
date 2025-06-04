# 🧩 Puzzle Decoder Race

## 🚀 Challenge Description

This project solves the **"Puzzle Decoder Race"** challenge.

The goal is to reconstruct a hidden message from multiple HTTP fragments that come with random delays. The program fetches all pieces, sorts them, and prints the complete message as fast as possible.

## ⚙️ Requirements

- Python **3.13**
- Docker

## 🛠️ Setup & Run

### 1. Install Dependencies

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Start Server

```bash
docker run -p 8080:8080 ifajardov/puzzle-server
```

### 3. Run Decoder

```bash
python decoder.py
```

## 🧠 Strategy

The solution uses **multiple workers running at the same time** to fetch fragments quickly:

- **20 workers** fetch different fragments simultaneously
- Each worker tries different fragment IDs
- When all pieces are found, the program stops and shows the message
- Uses Python's `asyncio` for speed

This approach is much faster than fetching fragments one by one.

## 🏁 Performance

- ✅ **Completed in under 1 second**
- ⏱ **Average time**: ~0.74 seconds