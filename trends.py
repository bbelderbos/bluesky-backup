import collections
import itertools

import pandas as pd
import streamlit as st
from decouple import config
from sqlalchemy import create_engine

BLUESKY_HANDLE = config("BLUESKY_HANDLE")


def main():
    conn = create_engine("sqlite:///posts.db")
    df = pd.read_sql(f'SELECT * FROM "{BLUESKY_HANDLE}";', conn)

    st.title("Bluesky stats")
    st.subheader("Daily activity")

    df["day"] = df["published"].str[:10]
    df_activity = pd.DataFrame(df.groupby(["day"]).count()["id"])
    df_activity.columns = ["# posts per day"]

    st.line_chart(df_activity)

    st.subheader("Most used tags")

    tags = df["text"].str.findall(r"#\w+").tolist()
    tags_flattened = (tag.lower() for tag in itertools.chain.from_iterable(tags))
    most_common_tags = collections.Counter(tags_flattened)

    df_tags = pd.DataFrame.from_dict(most_common_tags, orient="index")
    df_tags.columns = ["# used tags per tag"]
    st.bar_chart(df_tags)


if __name__ == "__main__":
    main()
