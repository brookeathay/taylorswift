import streamlit as st
import pandas as pd
import random

# --- PAGE SETUP ---
st.set_page_config(
    page_title="The Eras Bracket Challenge",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ERA PALETTES & METADATA ---
ERA_THEMES = {
    "taylor swift": {
        "bg_gradient": "linear-gradient(135deg, #1f2b1d 0%, #2f402c 100%)",
        "card_bg": "#243422",
        "accent": "#9dc183",
        "text_color": "#eef5ea",
        "glow": "rgba(157, 193, 131, 0.4)",
        "badge": "🌻 DEBUT ERA"
    },
    "fearless": {
        "bg_gradient": "linear-gradient(135deg, #2d240d 0%, #4a3b16 100%)",
        "card_bg": "#3d3011",
        "accent": "#f5c542",
        "text_color": "#fffbf0",
        "glow": "rgba(245, 197, 66, 0.4)",
        "badge": "✨ FEARLESS ERA"
    },
    "speak now": {
        "bg_gradient": "linear-gradient(135deg, #23122c 0%, #3e204d 100%)",
        "card_bg": "#2c1539",
        "accent": "#c084fc",
        "text_color": "#faf5ff",
        "glow": "rgba(192, 132, 252, 0.4)",
        "badge": "💜 SPEAK NOW ERA"
    },
    "red": {
        "bg_gradient": "linear-gradient(135deg, #2b0b0e 0%, #4c141a 100%)",
        "card_bg": "#3b0f14",
        "accent": "#ef4444",
        "text_color": "#fff1f2",
        "glow": "rgba(239, 68, 68, 0.4)",
        "badge": "🧣 RED ERA"
    },
    "1989": {
        "bg_gradient": "linear-gradient(135deg, #0d2235 0%, #173b5c 100%)",
        "card_bg": "#132d47",
        "accent": "#38bdf8",
        "text_color": "#f0f9ff",
        "glow": "rgba(56, 189, 248, 0.4)",
        "badge": "🕶 1989 ERA"
    },
    "reputation": {
        "bg_gradient": "linear-gradient(135deg, #0f0f0f 0%, #212121 100%)",
        "card_bg": "#181818",
        "accent": "#4ade80",
        "text_color": "#f5f5f5",
        "glow": "rgba(74, 222, 128, 0.35)",
        "badge": "🐍 REPUTATION ERA"
    },
    "lover": {
        "bg_gradient": "linear-gradient(135deg, #381528 0%, #5c2443 100%)",
        "card_bg": "#481b34",
        "accent": "#f472b6",
        "text_color": "#fdf2f8",
        "glow": "rgba(244, 114, 182, 0.4)",
        "badge": "💘 LOVER ERA"
    },
    "folklore": {
        "bg_gradient": "linear-gradient(135deg, #1c1d1a 0%, #30332e 100%)",
        "card_bg": "#252823",
        "accent": "#a8a29e",
        "text_color": "#f5f5f4",
        "glow": "rgba(168, 162, 158, 0.3)",
        "badge": "🌲 FOLKLORE ERA"
    },
    "evermore": {
        "bg_gradient": "linear-gradient(135deg, #2b1810 0%, #47271a 100%)",
        "card_bg": "#381f14",
        "accent": "#fb923c",
        "text_color": "#fff7ed",
        "glow": "rgba(251, 146, 60, 0.4)",
        "badge": "🍂 EVERMORE ERA"
    },
    "midnights": {
        "bg_gradient": "linear-gradient(135deg, #090e24 0%, #131c47 100%)",
        "card_bg": "#0f1638",
        "accent": "#818cf8",
        "text_color": "#eef2ff",
        "glow": "rgba(129, 140, 248, 0.45)",
        "badge": "🌙 MIDNIGHTS ERA"
    },
    "the tortured poets department": {
        "bg_gradient": "linear-gradient(135deg, #171513 0%, #2b2724 100%)",
        "card_bg": "#211e1c",
        "accent": "#d6d3d1",
        "text_color": "#fafaf9",
        "glow": "rgba(214, 211, 209, 0.35)",
        "badge": "🖋 TTPD ERA"
    },
    "life of a showgirl": {
        "bg_gradient": "linear-gradient(135deg, #2e1026 0%, #521d45 100%)",
        "card_bg": "#3d1633",
        "accent": "#e879f9",
        "text_color": "#fdf4ff",
        "glow": "rgba(232, 121, 249, 0.4)",
        "badge": "🎭 SHOWGIRL ERA"
    }
}

DEFAULT_THEME = {
    "bg_gradient": "linear-gradient(135deg, #111827 0%, #1f2937 100%)",
    "card_bg": "#1e293b",
    "accent": "#f43f5e",
    "text_color": "#f8fafc",
    "glow": "rgba(244, 63, 94, 0.4)",
    "badge": "👑 THE ERAS TOUR"
}

ALBUM_DATA = {
    "taylor swift": (
        "🌻 You're heartfelt and loyal. You believe in fairytales, handwritten notes, and love that feels forever.",
        "Olivia Dean", "The Daydream Believer"),
    "fearless": ("✨ You're brave in love. You run toward butterflies, not away from them.", "Sabrina Carpenter",
                 "The Golden Romantic"),
    "speak now": (
        "💜 You're dramatic in the best way. You feel everything deeply and say what others are too scared to.",
        "Conan Gray", "The Confessional Poet"),
    "red": ("🧣 You love hard and remember everything. Passionate, nostalgic, and a little chaotic.", "Gracie Abrams",
            "The Passionate Archivist"),
    "1989": ("🕶 You're confident and independent. Reinvention looks good on you.", "Tate McRae", "The Pop Visionary"),
    "reputation": ("🐍 You're bold, magnetic, and misunderstood. You protect your heart but love fiercely.",
                   "Stray Kids", "The Untouchable Icon"),
    "lover": ("💘 You're soft but strong. Romantic, hopeful, and unapologetically emotional.", "ROSÉ",
              "The Hopeless Romantic"),
    "folklore": ("🌲 You're introspective and poetic. You find beauty in quiet moments and untold stories.", "Bon Iver",
                 "The Story Weaver"),
    "evermore": (
        "🍂 You're thoughtful and emotionally layered. You sit with your feelings instead of running from them.",
        "Lana Del Rey", "The Autumn Philosopher"),
    "midnights": ("🌙 You're a late-night thinker. Self-aware, reflective, and a little mysterious.", "Djo",
                  "The Midnight Mastermind"),
    "the tortured poets department": (
        "🖋 You're intense and expressive. You turn heartbreak into art and overthink in italics.", "Gracie Abrams",
        "The Tortured Wordsmith"),
    "life of a showgirl": (
        "🎭 You live for the spotlight but feel everything when the curtain falls. Glitter on the outside, depth on the inside.",
        "Chappell Roan", "The Spotlight Siren")
}

EGGS = [
    "🐍 A snake slithers by... Reputation energy detected.",
    "🕯 A cardigan appears out of nowhere. Folklore found you.",
    "💄 You check the mirror. Red lipstick era activated.",
    "🌙 It's 2:13 AM. You should be sleeping. You're not.",
    "📓 You found a hidden lyric in the margins.",
    "🎭 The spotlight flickers. Showgirl mode watching.",
    "🧣 You smell autumn air and unfinished business.",
    "💎 A mastermind never reveals their strategy."
]


# --- LOAD DATA ---
@st.cache_data
def load_songs():
    try:
        return pd.read_csv("songs.csv")
    except FileNotFoundError:
        st.error("⚠️ `songs.csv` not found. Please place it in the same directory as this file.")
        st.stop()


songs_df = load_songs()
all_albums = list(songs_df['Album'].unique())

# --- SESSION STATE INITIALIZATION ---
if "phase" not in st.session_state:
    st.session_state.phase = "SELECT_ALBUM"
    st.session_state.album_ratings = {}  # {album_name: avg_score}
    st.session_state.all_song_ratings = {}  # {song_name: rating}
    st.session_state.album_winners = []  # [top_song_1, top_song_2, ...]
    st.session_state.lucky_13_count = 0
    st.session_state.current_album = None
    st.session_state.bracket_list = []
    st.session_state.bracket_winner = None
    st.session_state.bracket_step = 1
    st.session_state.final_winner = None
    st.session_state.recent_egg = None


# --- DYNAMIC CSS INJECTION ---
def get_current_theme():
    if st.session_state.current_album:
        return ERA_THEMES.get(st.session_state.current_album.lower(), DEFAULT_THEME)
    return DEFAULT_THEME


theme = get_current_theme()

st.markdown(f"""
    <style>
        .stApp {{
            background: {theme['bg_gradient']};
            color: {theme['text_color']};
            font-family: 'Helvetica Neue', Arial, sans-serif;
            transition: background 0.6s ease;
        }}
        .era-card {{
            background-color: {theme['card_bg']};
            border: 1px solid {theme['accent']};
            box-shadow: 0 4px 20px {theme['glow']};
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 20px;
        }}
        .title-text {{
            color: {theme['text_color']} !important;
            font-weight: 800;
            letter-spacing: -0.5px;
        }}
        .era-badge {{
            display: inline-block;
            background: {theme['accent']};
            color: #111;
            padding: 4px 12px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.85rem;
            margin-bottom: 12px;
        }}
        div.stButton > button {{
            background-color: {theme['accent']};
            color: #0d1117;
            border: none;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.6rem 1.4rem;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        div.stButton > button:hover {{
            transform: scale(1.02);
            box-shadow: 0 0 16px {theme['glow']};
        }}
    </style>
""", unsafe_allow_html=True)


def trigger_random_easter_egg():
    if random.random() < 0.25:
        egg = random.choice(EGGS)
        st.session_state.recent_egg = egg
        st.toast(egg, icon="💎")


# ==============================================================================
# SCREEN 1: ERA SELECTOR
# ==============================================================================
if st.session_state.phase == "SELECT_ALBUM":
    st.session_state.current_album = None

    st.markdown('<div class="era-badge">👑 ERA TOURNAMENT HUB</div>', unsafe_allow_html=True)
    st.title("The Ultimate Taylor Swift Bracket")
    st.write(
        "Rate songs across Taylor's discography on a 13-point scale. Resolve ties through head-to-head showdowns and uncover your true Era personality.")

    remaining_albums = [a for a in all_albums if a not in st.session_state.album_ratings]

    col_main, col_stats = st.columns([2, 1])

    with col_main:
        if not remaining_albums:
            st.success("🎉 You've rated every album! The stage is set for the Final Era Showdown.")
            if st.button("Enter The Ultimate Showdown 🏆", use_container_width=True):
                st.session_state.bracket_list = list(st.session_state.album_winners)
                random.shuffle(st.session_state.bracket_list)
                st.session_state.bracket_winner = st.session_state.bracket_list[0]
                st.session_state.bracket_step = 1
                st.session_state.phase = "FINAL_BRACKET"
                st.rerun()
        else:
            selected = st.selectbox("Select an Era to explore:", remaining_albums)

            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button(f"Rate '{selected}' 🎵", use_container_width=True):
                    trigger_random_easter_egg()
                    st.session_state.current_album = selected
                    st.session_state.phase = "RATE_ALBUM"
                    st.rerun()
            with c2:
                if st.session_state.album_winners:
                    if st.button("Finish Early & Go to Finals 🏆", use_container_width=True):
                        st.session_state.bracket_list = list(st.session_state.album_winners)
                        random.shuffle(st.session_state.bracket_list)
                        st.session_state.bracket_winner = st.session_state.bracket_list[0]
                        st.session_state.bracket_step = 1
                        st.session_state.phase = "FINAL_BRACKET"
                        st.rerun()

    with col_stats:
        st.markdown('<div class="era-card">', unsafe_allow_html=True)
        st.subheader("Your Tour Progress")
        st.write(f"**Eras Completed:** {len(st.session_state.album_ratings)} / {len(all_albums)}")
        st.write(f"**Lucky 13s Awarded:** {st.session_state.lucky_13_count} 💎")

        if st.session_state.album_ratings:
            st.divider()
            st.write("**Top Rated Era So Far:**")
            top_era = max(st.session_state.album_ratings, key=st.session_state.album_ratings.get)
            st.write(f"✨ *{top_era}* ({st.session_state.album_ratings[top_era]:.2f}/13)")
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SCREEN 2: RATE SONGS IN CHOSEN ALBUM
# ==============================================================================
elif st.session_state.phase == "RATE_ALBUM":
    album = st.session_state.current_album
    badge_label = ERA_THEMES.get(album.lower(), DEFAULT_THEME)["badge"]

    st.markdown(f'<div class="era-badge">{badge_label}</div>', unsafe_allow_html=True)
    st.title(f"Rating: {album}")
    st.write(
        "Score each track on a scale from **1 to 13** (Taylor's lucky number). Awarding a **13** adds to your Lucky 13 counter!")

    songs_in_album = songs_df[songs_df['Album'] == album]["Song"].tolist()

    with st.form(key="rating_form"):
        ratings = {}
        # Render songs in a two-column grid for cleaner layout
        col1, col2 = st.columns(2)
        for idx, song in enumerate(songs_in_album):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                ratings[song] = st.slider(
                    f"✨ {song}",
                    min_value=1,
                    max_value=13,
                    value=10,
                    key=f"rating_{song}"
                )

        submitted = st.form_submit_button("Lock In Ratings 🔒", use_container_width=True)

    if submitted:
        # Detect Lucky 13s
        awarded_13s = sum(1 for score in ratings.values() if score == 13)
        st.session_state.lucky_13_count += awarded_13s
        if awarded_13s > 0:
            st.balloons()
            st.toast(f"💎 Lucky 13! Taylor would approve. (+{awarded_13s} added)", icon="✨")

        st.session_state.all_song_ratings.update(ratings)

        # Calculate Album Average
        avg_score = sum(ratings.values()) / len(ratings)
        st.session_state.album_ratings[album] = avg_score

        # Identify Top Songs
        max_score = max(ratings.values())
        top_songs = [s for s, r in ratings.items() if r == max_score]

        if len(top_songs) > 1:
            # Trigger Tiebreaker
            st.session_state.bracket_list = list(top_songs)
            random.shuffle(st.session_state.bracket_list)
            st.session_state.bracket_winner = st.session_state.bracket_list[0]
            st.session_state.bracket_step = 1
            st.session_state.phase = "ALBUM_TIEBREAKER"
        else:
            # Single winner
            st.session_state.album_winners.append(top_songs[0])
            st.session_state.phase = "SELECT_ALBUM"
            st.toast(f"Top track for {album}: {top_songs[0]}! 👑")
        st.rerun()

# ==============================================================================
# SCREEN 3: HEAD-TO-HEAD BRACKET (TIEBREAKER & FINALS)
# ==============================================================================
elif st.session_state.phase in ["ALBUM_TIEBREAKER", "FINAL_BRACKET"]:
    is_final = (st.session_state.phase == "FINAL_BRACKET")
    contenders = st.session_state.bracket_list
    current_champ = st.session_state.bracket_winner
    step = st.session_state.bracket_step

    if is_final:
        st.markdown('<div class="era-badge">🏆 THE ULTIMATE ERA SHOWDOWN</div>', unsafe_allow_html=True)
        st.title("Grand Finale Bracket")
        st.write("The top songs from each of your rated albums now clash head-to-head for the crown!")
    else:
        album = st.session_state.current_album
        st.markdown(f'<div class="era-badge">⚡ {album.upper()} TIEBREAKER</div>', unsafe_allow_html=True)
        st.title("Sudden Death Matchup")
        st.write("Multiple songs tied for highest score. Pick your preference to crown the album winner:")

    if step < len(contenders):
        challenger = contenders[step]

        # Matchup Card Container
        st.markdown('<div class="era-card">', unsafe_allow_html=True)
        st.subheader(f"Round {step} of {len(contenders) - 1}")

        c1, c_vs, c2 = st.columns([5, 1, 5])

        with c1:
            st.markdown(f"### 👑 Current Leader\n**{current_champ}**")
            if st.button(f"Vote for '{current_champ}'", key=f"champ_{step}", use_container_width=True):
                trigger_random_easter_egg()
                st.session_state.bracket_step += 1
                st.rerun()

        with c_vs:
            st.markdown("<h2 style='text-align: center; margin-top: 25px;'>VS</h2>", unsafe_allow_html=True)

        with c2:
            st.markdown(f"### ⚡ Challenger\n**{challenger}**")
            if st.button(f"Vote for '{challenger}'", key=f"chal_{step}", use_container_width=True):
                trigger_random_easter_egg()
                st.session_state.bracket_winner = challenger
                st.session_state.bracket_step += 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Bracket completed
        winner = current_champ
        if not is_final:
            st.session_state.album_winners.append(winner)
            st.session_state.phase = "SELECT_ALBUM"
            st.toast(f"Winner declared: {winner}! 👑", icon="✨")
            st.rerun()
        else:
            st.session_state.final_winner = winner
            st.session_state.phase = "RESULTS"
            st.rerun()

# ==============================================================================
# SCREEN 4: RESULTS & MASTERMIND MODE
# ==============================================================================
elif st.session_state.phase == "RESULTS":
    st.balloons()
    st.markdown('<div class="era-badge">✨ YOUR ERA HAS BEEN CHOSEN</div>', unsafe_allow_html=True)
    st.title("Your Era Breakdown")

    best_album = max(st.session_state.album_ratings, key=st.session_state.album_ratings.get)
    best_score = st.session_state.album_ratings[best_album]
    meta = ALBUM_DATA.get(best_album.lower(), (
        "You have elite, unparalleled taste across every single era.",
        "Taylor Swift",
        "The Pop Visionary"
    ))

    # Personality Spotlight Card
    st.markdown(f"""
        <div class="era-card">
            <h2 class="title-text">👑 Favorite Song Overall: {st.session_state.final_winner}</h2>
            <h3 style="color: {theme['accent']};">💖 Favorite Era: {best_album} (Avg: {best_score:.2f}/13)</h3>
            <p style="font-size: 1.15rem; font-style: italic; margin-top: 15px;">"{meta[0]}"</p>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
            <p><strong>👑 Swiftie Title:</strong> {meta[2]}</p>
            <p><strong>🎧 Recommended Artist:</strong> {meta[1]}</p>
        </div>
    """, unsafe_allow_html=True)

    # Mastermind Mode Check
    all_rated = len(st.session_state.album_ratings) == len(all_albums)
    is_mastermind = (st.session_state.lucky_13_count >= 13 and best_score >= 12 and all_rated)

    if is_mastermind:
        st.markdown("""
            <div style="background-color: #022c22; border: 2px solid #34d399; border-radius: 12px; padding: 20px; margin-top: 20px;">
                <h2 style="color: #34d399; margin-top: 0;">⚠️ MASTERMIND MODE ACTIVATED ⚠️</h2>
                <p>You didn’t just rate songs... You calculated outcomes. You noticed patterns. You played strategically.</p>
                <p><strong>👑 Swiftie Rank:</strong> The Architect | <strong>💎 Rarity:</strong> Legendary | <strong>🧠 Era Energy:</strong> Mastermind</p>
                <p><em>You were never guessing. You were always in control.</em></p>
            </div>
        """, unsafe_allow_html=True)

    # Top Songs Table & Playlist Export
    st.subheader("Your Top Tracks Playlist")
    sorted_songs = sorted(st.session_state.all_song_ratings.items(), key=lambda x: x[1], reverse=True)[:50]
    export_df = pd.DataFrame(sorted_songs, columns=["Song", "Rating"])

    col_tbl, col_dl = st.columns([3, 1])
    with col_tbl:
        st.dataframe(export_df, use_container_width=True, hide_index=True)
    with col_dl:
        csv_data = export_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Top 50 CSV",
            data=csv_data,
            file_name="my_top_taylor_songs.csv",
            mime="text/csv",
            use_container_width=True
        )
        if st.button("Start Fresh 🔄", use_container_width=True):
            st.session_state.clear()
            st.rerun()