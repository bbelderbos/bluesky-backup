# README: Bluesky Backup Script

## Overview

This script fetches posts from a Bluesky account using the Bluesky API and backs them up into a SQLite database. It avoids duplicates and fetches all posts on the first run, then retrieves only new posts on subsequent runs.

---

## Setup

1. **Set Up the Virtual Environment**:
   - Run the following command to create a virtual environment and install dependencies:
     ```bash
     uv sync
     ```

2. **Environment Variables**:
   - Copy `.env-template` to `.env`:
     ```bash
     cp .env-template .env
     ```
   - Set the required variables in `.env`:
     ```env
     API_TOKEN=<Your Bluesky API Token>
     BLUESKY_HANDLE=<Your Bluesky Handle>
     ```

3. **Run the Script**:
   - Use `uv` (or `python`) to run the script:
     ```bash
     uv run python backup_posts.py
     ```

---

## Notes
- The SQLite database will be stored in the same directory as the script, named `posts.db`.
- On the first run:
  - All posts from the Bluesky account will be fetched.
  - This may take longer depending on the total number of posts.
- On subsequent runs:
  - Only new posts (up to 100, the API's limit) will be retrieved.
- I kept it simple for starters, so this does not include replies to posts (including your own), reposts, likes (stats) and media file links. More than happy to receive contributions to add these features!
- The database structure is automatically created on the first run.
- I included a GitHub Action to run this automatically every day.
---

There you go, now you'll have an automated backup of your Bluesky posts! 🚀
