from datetime import datetime
from pathlib import Path

import sqlite_utils
from atproto import Client
from atproto_client.models.app.bsky.feed.defs import FeedViewPost
from decouple import config
from sqlite_utils.db import Table

API_TOKEN = config("API_TOKEN")
BLUESKY_HANDLE = config("BLUESKY_HANDLE")
DB_FILE = "posts.db"
DB = sqlite_utils.Database(DB_FILE)
MAX_POSTS_API = 100

client = Client()
client.login(BLUESKY_HANDLE, API_TOKEN)


def _fetch_all_entries(
    *, use_cursor: bool = False, limit: int = MAX_POSTS_API
) -> list[FeedViewPost]:
    all_entries = []
    cursor = None

    if not use_cursor:
        data = client.get_author_feed(actor=BLUESKY_HANDLE, limit=limit)
        return data.feed

    while True:
        data = client.get_author_feed(
            actor=BLUESKY_HANDLE, limit=MAX_POSTS_API, cursor=cursor
        )
        entries = data.feed
        all_entries.extend(entries)

        cursor = getattr(data, "cursor", None)
        if not cursor or not entries:
            break

    return all_entries


def _own_post(entry: FeedViewPost) -> bool:
    return entry.post.record.reply is None and entry.post.viewer.repost is None


def _is_new_db() -> bool:
    return not Path(DB_FILE).exists() or Path(DB_FILE).stat().st_size == 0


def _get_all_ids(table: Table) -> set[str]:
    return {row["id"] for row in table.rows}


def insert_new_posts() -> None:
    """Upsert posts into sqlite db, if first time retrieve all posts"""
    entries = _fetch_all_entries(use_cursor=_is_new_db())

    rows = [
        {
            "id": entry.post.cid,
            "text": entry.post.record.text,
            "published": datetime.fromisoformat(
                entry.post.record.created_at.replace("Z", "+00:00")
            ),
        }
        for entry in entries
        if _own_post(entry)
    ]

    table = DB[BLUESKY_HANDLE]
    # extra check for mypy
    assert isinstance(table, sqlite_utils.db.Table), f"{BLUESKY_HANDLE} is not a Table"

    existing_ids = _get_all_ids(table)
    table.upsert_all(rows, pk="id")
    current_ids = _get_all_ids(table)

    new_ids = current_ids - existing_ids
    if new_ids:
        print(f"New posts upserted: {len(new_ids)}")
    else:
        print("No new posts were upserted.")


if __name__ == "__main__":
    insert_new_posts()
