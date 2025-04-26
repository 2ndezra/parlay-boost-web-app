
import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
from datetime import datetime
import time

def fetch_player_log_with_retry(player_id, max_attempts=5, delay=3):
    for attempt in range(max_attempts):
        try:
            logs = []
            current_year = datetime.today().year
            for year in range(current_year, 2009, -1):
                season = f"{year}-{str(year+1)[-2:]}"
                log = playergamelog.PlayerGameLog(
                    player_id=player_id,
                    season=season,
                    season_type_all_star='Regular Season'
                )
                df = log.get_data_frames()[0]
                if not df.empty:
                    logs.append(df)
            return pd.concat(logs, ignore_index=True)
        except Exception as e:
            st.warning(f"Retry {attempt+1}/{max_attempts}: {e}")
            time.sleep(delay)
    st.error("Failed to fetch player logs after multiple attempts.")
    return pd.DataFrame()

# Use this in your app:
# player_id = ...
# df = fetch_player_log_with_retry(player_id)
