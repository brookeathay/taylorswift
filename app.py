import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Taylor Swift Song Bracket", page_icon="✨", layout="centered")


# --- DATA HELPERS ---
@st.cache_data
def load_songs():
    try:
        return pd.read_csv("songs.csv")
    except FileNotFoundError:
        st.error("Missing `songs.csv` in the root folder.")
        st.stop()


songs_df = load_songs()
albums = list(songs_df['Album'].unique())

ALBUM_DATA = {
    "taylor swift": ("🌻 You're heartfelt and loyal. You believe in fairytales and handwritten notes.", "Olivia Dean",
                     "The Daydream Believer"),
    "fearless": ("✨ You're brave in love. You run toward butterflies, not away from them.", "Sabrina Carpenter",
                 "The Golden Romantic"),
    "speak now": ("💜 You're dramatic in the best way. You feel everything deeply.", "Conan Gray",
                  "The Confessional Poet"),
    "red": ("🧣 You love hard and remember everything. Passionate, nostalgic, and chaotic.", "Gracie Abrams",
            "The Passionate Archivist"),
    "1989": ("🕶 You're confident and independent. Reinvention looks good on you.", "Tate McRae", "The Pop Visionary"),
    "reputation": ("🐍 You're bold, magnetic, and misunderstood. You protect your heart.", "Stray Kids",
                   "The Untouchable Icon"),
    "lover": ("💘 You're soft but strong. Romantic, hopeful, and unapologetically emotional.", "ROSÉ",
              "The Hopeless Romantic"),
    "folklore": ("🌲 You're introspective and poetic. You find beauty in quiet moments.", "Bon Iver",
                 "The Story Weaver"),
    "evermore": ("🍂 You're thoughtful and emotionally layered. You sit with your feelings.", "Lana Del Rey",
                 "The Autumn Philosopher"),
    "midnights": ("🌙 You're a late-night thinker. Self-aware, reflective, and a little mysterious.", "Djo",
                  "The Midnight Mastermind"),
    "the tortured poets department": ("🖋 You're intense and expressive. You turn heartbreak into art.", "Gracie Abrams",
                                      "The Tortured Wordsmith"),
    "life of a showgirl": ("🎭 Glitter on the outside, depth on the inside. You live for the spotlight.",
                           "Chappell Roan", "The Spotlight Siren")
}

EGGS = [
    "🐍 A snake slithers by... Reputation energy detected.",
    "🕯 A cardigan appears out of nowhere. Folklore found you.",
    "💄 You check the mirror. Red lipstick era activated.",
    "🌙 It's 2:13 AM. You should be sleeping. You're not.",
    "📓 You found a hidden lyric in the margins.",
    "🧣 You smell autumn air and unfinished business."
]


def check_easter_egg():
    if random.random() < 0.25:
        st.toast(random.choice(EGGS), icon="💎")


# --- SESSION STATE ---
if "phase" not in st.session_state:
    st.session_state.phase = "SELECT_ALBUM"
    st.session_state.album_ratings = {}  # {album: avg}
    st.session_state.all_song_ratings = {}  # {song: rating}
    st.session_state.album_winners = []  # [top_song, ...]
    st.session_state.lucky_13_count = 0
    st.session_state.current_album = None
    st.session_state.bracket_list = []
    st.session_state.bracket_winner = None
    st.session_state.bracket_step = 1

# --- SCREEN 1: SELECT ALBUM ---
if st.session_state.phase == "SELECT_ALBUM":
    st.title("✨ Taylor Swift Era Ranker ✨")
    st.write("Rate songs across albums to find your true #1 song and era personality.")

    remaining = [a for a in albums if a not in st.session_state.album_ratings]

    if not remaining:
        st.success("All albums rated!")
        if st.button("Proceed to Final Showdown 🏆"):
            st.session_state.bracket_list = list(st.session_state.album_winners)
            random.shuffle(st.session_state.bracket_list)
            st.session_state.bracket_winner = st.session_state.bracket_list[0]
            st.session_state.bracket_step = 1
            st.session_state.phase = "FINAL_BRACKET"
            st.rerun()
    else:
        selected = st.selectbox("Choose an Era to rate:", remaining)
        if st.button(f"Rate {selected} 🎵"):
            check_easter_egg()
            st.session_state.current_album = selected
            st.session_state.phase = "RATE_ALBUM"
            st.rerun()

        if st.session_state.album_winners:
            st.divider()
            if st.button("Finish now and jump to Final Showdown 🎤"):
                st.session_state.bracket_list = list(st.session_state.album_winners)
                random.shuffle(st.session_state.bracket_list)
                st.session_state.bracket_winner = st.session_state.bracket_list[0]
                st.session_state.bracket_step = 1
                st.session_state.phase = "FINAL_BRACKET"
                st.rerun()

# --- SCREEN 2: RATE SONGS ---
elif st.session_state.phase == "RATE_ALBUM":
    album = st.session_state.current_album
    st.title(f"🎵 Rating: {album}")
    st.caption("Rate each track from 1 to 13 (Taylor's lucky number).")

    songs_in_album = songs_df[songs_df['Album'] == album]["Song"].tolist()

    with st.form("rating_form"):
        ratings = {}
        for song in songs_in_album:
            ratings[song] = st.slider(song, min_value=1, max_value=13, value=10)
        submitted = st.form_submit_button("Submit Ratings ✨")

    if submitted:
        lucky_count = sum(1 for v in ratings.values() if v == 13)
        st.session_state.lucky_13_count += lucky_count
        st.session_state.all_song_ratings.update(ratings)

        avg_score = sum(ratings.values()) / len(ratings)
        st.session_state.album_ratings[album] = avg_score

        # Find top tracks
        max_score = max(ratings.values())
        top_songs = [s for s, r in ratings.items() if r == max_score]

        if len(top_songs) > 1:
            st.session_state.bracket_list = list(top_songs)
            random.shuffle(st.session_state.bracket_list)
            st.session_state.bracket_winner = st.session_state.bracket_list[0]
            st.session_state.bracket_step = 1
            st.session_state.phase = "ALBUM_TIEBREAKER"
        else:
            st.session_state.album_winners.append(top_songs[0])
            st.session_state.phase = "SELECT_ALBUM"
            st.toast(f"Top track for {album}: {top_songs[0]}!")
        st.rerun()

# --- SCREEN 3: HEAD-TO-HEAD TIEBREAKER ---
elif st.session_state.phase in ["ALBUM_TIEBREAKER", "FINAL_BRACKET"]:
    is_final = st.session_state.phase == "FINAL_BRACKET"
    st.title("⚔️ Head-to-Head Showdown" if not is_final else "🏆 The Ultimate Era Showdown 🏆")

    contenders = st.session_state.bracket_list
    current_winner = st.session_state.bracket_winner
    step = st.session_state.bracket_step

    if step < len(contenders):
        challenger = contenders[step]
        st.subheader("Which song wins?")
        col1, col2 = st.columns(2)

        with col1:
            if st.button(current_winner, use_container_width=True):
                st.session_state.bracket_step += 1
                st.rerun()
        with col2:
            if st.button(challenger, use_container_width=True):
                st.session_state.bracket_winner = challenger
                st.session_state.bracket_step += 1
                st.rerun()
    else:
        # Bracket done
        winner = current_winner
        if not is_final:
            st.session_state.album_winners.append(winner)
            st.session_state.phase = "SELECT_ALBUM"
            st.toast(f"Winner: {winner}!")
            st.rerun()
        else:
            st.session_state.final_song = winner
            st.session_state.phase = "RESULTS"
            st.rerun()

# --- SCREEN 4: RESULTS & PERSONALITY ---
elif st.session_state.phase == "RESULTS":
    st.title("✨ YOUR ERA RESULTS ✨")

    # Favorite song
    st.subheader(f"👑 #1 Taylor Swift Song: **{st.session_state.final_song}**")

    # Favorite album
    best_album = max(st.session_state.album_ratings, key=st.session_state.album_ratings.get)
    best_score = st.session_state.album_ratings[best_album]
    st.write(f"💖 **Favorite Album:** {best_album} (avg: {best_score:.2f}/13)")

    # Personality message
    meta = ALBUM_DATA.get(best_album.lower(), ("You have elite taste. 🎶", "Taylor Swift", "The Visionary"))
    st.info(f"{meta[0]}\n\n**Swiftie Title:** {meta[2]}  \n**Recommended Artist:** {meta[1]}")

    # Mastermind check
    if (st.session_state.lucky_13_count >= 13 and best_score >= 12 and len(st.session_state.album_ratings) == len(
            albums)):
        st.warning("🧠 **MASTERMIND MODE ACTIVATED**: You calculated outcomes. You were always in control.")

    # Top tracks download
    st.divider()
    top_50 = sorted(st.session_state.all_song_ratings.items(), key=lambda x: x[1], reverse=True)[:50]
    df_out = pd.DataFrame(top_50, columns=["Song", "Rating"])

    st.write("### Your Top Songs")
    st.dataframe(df_out, hide_index=True)
    st.download_button("📥 Download Top Songs CSV", df_out.to_csv(index=False), "taylor_top_tracks.csv", "text/csv")

    if st.button("Start Over"):
        st.session_state.clear()
        st.rerun()