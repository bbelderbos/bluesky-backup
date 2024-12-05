# Bluesky Backup Script

## Overview

The `backup_posts.py` script fetches posts from a Bluesky account using the Bluesky API and backs them up into a SQLite database. 

It avoids duplicates and fetches all posts on the first run, then retrieves only new posts on subsequent runs.

There is also a `trends.py` script to show some basic stats about daily usage and tags.

---

## Setup

1. **Run the project with uv**:
   - Run the following command to create a virtual environment and install dependencies:
     ```bash
     uv sync
     ```

2. **Set environment variables**:
   - Copy `.env-template` to `.env`:
     ```bash
     cp .env-template .env
     ```
   - Set the required variables in `.env`:
     ```env
     API_TOKEN=<Your Bluesky API Token>
     BLUESKY_HANDLE=<Your Bluesky Handle>
     ```

3. **Make a backup**:
   - Use `uv` (or `python`) to run the script:
     ```bash
     uv run python backup_posts.py
     ```
     
This repo includes a [GitHub Action](https://github.com/bbelderbos/bluesky-backup/blob/main/.github/workflows/backup.yaml) to run this automatically every day.

4. **Look at Trends**:
   - Use `uv` (or `python`) to install extra dependencies and run the trends script which uses Streamlit:
     ```bash
     uv sync --group reporting
     uv run streamlit run trends.py
     ```

(I clearly like talking about Python 🐍 😍)

<img width="829" alt="image" src="https://github.com/user-attachments/assets/920043ae-3c70-4cd6-b38d-a8ba5bfde4ba">

---

## Notes
- The SQLite database will be stored in the same directory as the script, named `posts.db`.
- On the first run:
  - All posts from the Bluesky account will be fetched.
  - This may take longer depending on the total number of posts.
- On subsequent runs:
  - Only new posts (up to 100, the API's limit) will be retrieved.
- I kept it simple for starters, so this does not include replies to posts (including your own), reposts, likes (stats) and media file links. More than happy to receive contributions to make this better ...
- The DB + its structure is automatically created on the first run.
- Original idea: [Mastodon Backup Script](https://github.com/bbelderbos/mastodon-backup).

---

There you go, now you can have an automated backup of your Bluesky posts! 🚀
