# 🧩 Puzzle Decoder Race

## 🚀 Challenge Description

This project solves the **"Puzzle Decoder Race"** challenge.

The goal is to reconstruct a hidden message from multiple HTTP fragments that come with random delays. The program fetches all pieces, sorts them, and prints the complete message as fast as possible.

## ⚙️ Requirements

- uv
- Python **3.13**
- Docker

## 🛠️ Setup & Run

### 1. Install Dependencies

First, we need to install **uv**, a Python dependency manager from Astral that allows us to manage dependencies and run files in an isolated virtual environment, separate from the global Python installation.

**Install uv:** Follow the installation guide at [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)

Once uv is installed, run the following commands:

```bash
# Create a virtual environment with Python 3.13
uv venv --python 3.13

# Activate the virtual environment
source .venv/bin/activate

# Install project dependencies
uv sync --locked
```

### 2. Start Server

```bash
docker run -p 8080:8080 ifajardov/puzzle-server
```

### 3. Run Decoder

```bash
uv run decoder.py
```

## 🧠 Strategy

The solution uses **multiple workers running at the same time** to fetch fragments quickly:

- **30 workers** fetch different fragments simultaneously
- Each worker tries different fragment IDs
- a separate worker is in charge of verifying when the puzzle is complete.
- When all pieces are found, the program stops and shows the message
- Uses Python's `asyncio` for speed

This approach is much faster than fetching fragments one by one.

## 🏁 Performance

- ✅ **Completed in under 1 second**
- ⏱ **Average time**: ~0.74 seconds
