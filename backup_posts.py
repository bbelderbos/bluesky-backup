import sys
from datetime import datetime

import sqlite_utils
from atproto import Client
from decouple import config

API_TOKEN = config("API_TOKEN")
BLUESKY_HANDLE = config("BLUESKY_HANDLE")
DB = sqlite_utils.Database("posts.db")


def _fetch_all_entries(client, handle, limit=100):
    all_entries = []
    cursor = None

    while True:
        data = client.get_author_feed(actor=handle, limit=limit, cursor=cursor)
        entries = data.feed
        all_entries.extend(entries)

        cursor = getattr(data, "cursor", None)
        if not cursor or not entries:
            break

    return all_entries


def insert_new_posts(handle, token=API_TOKEN):
    client = Client()
    client.login(handle, token)

    entries = _fetch_all_entries(client, handle)
    rows = [
        {
            "id": entry.post.cid,
            "text": entry.post.record.text,
            "published": datetime.fromisoformat(
                entry.post.record.created_at.replace("Z", "+00:00")
            ),
        }
        for entry in entries
        # Skip replies and reposts
        if entry.post.record.reply is None and entry.post.viewer.repost is None
    ]

    DB[handle].upsert_all(rows, pk="id")


if __name__ == "__main__":
    handle = sys.argv[1] if len(sys.argv) == 2 else BLUESKY_HANDLE
    insert_new_posts(handle)
