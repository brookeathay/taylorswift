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

# --- LIGHT & PASTEL ERA PALETTES ---
ERA_THEMES = {
    "taylor swift": {
        "bg_gradient": "linear-gradient(135deg, #f3f8f1 0%, #e1edd9 100%)",
        "card_bg": "#ffffff",
        "accent": "#4a7c59",
        "accent_light": "#e8f5e9",
        "text_color": "#233324",
        "badge_bg": "#c8e6c9",
        "badge_text": "#1b5e20",
        "shadow": "rgba(74, 124, 89, 0.15)",
        "badge": "🌻 DEBUT ERA"
    },
    "fearless": {
        "bg_gradient": "linear-gradient(135deg, #fffcf0 0%, #faecc7 100%)",
        "card_bg": "#ffffff",
        "accent": "#b8860b",
        "accent_light": "#fef9e7",
        "text_color": "#3d3000",
        "badge_bg": "#ffe082",
        "badge_text": "#5d4037",
        "shadow": "rgba(184, 134, 11, 0.18)",
        "badge": "✨ FEARLESS ERA"
    },
    "speak now": {
        "bg_gradient": "linear-gradient(135deg, #faf5ff 0%, #edd8fc 100%)",
        "card_bg": "#ffffff",
        "accent": "#8a2be2",
        "accent_light": "#f5ebfc",
        "text_color": "#33124d",
        "badge_bg": "#e1bee7",
        "badge_text": "#4a148c",
        "shadow": "rgba(138, 43, 226, 0.15)",
        "badge": "💜 SPEAK NOW ERA"
    },
    "red": {
        "bg_gradient": "linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%)",
        "card_bg": "#ffffff",
        "accent": "#c53030",
        "accent_light": "#ffebee",
        "text_color": "#4a0e17",
        "badge_bg": "#ffcdd2",
        "badge_text": "#b71c1c",
        "shadow": "rgba(197, 48, 48, 0.15)",
        "badge": "🧣 RED ERA"
    },
    "1989": {
        "bg_gradient": "linear-gradient(135deg, #f0f9ff 0%, #cbebfe 100%)",
        "card_bg": "#ffffff",
        "accent": "#0284c7",
        "accent_light": "#e0f2fe",
        "text_color": "#0c4a6e",
        "badge_bg": "#bae6fd",
        "badge_text": "#0369a1",
        "shadow": "rgba(2, 132, 199, 0.15)",
        "badge": "🕶 1989 ERA"
    },
    "reputation": {
        "bg_gradient": "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)",
        "card_bg": "#ffffff",
        "accent": "#1e293b",
        "accent_light": "#f1f5f9",
        "text_color": "#0f172a",
        "badge_bg": "#cbd5e1",
        "badge_text": "#0f172a",
        "shadow": "rgba(15, 23, 42, 0.12)",
        "badge": "🐍 REPUTATION ERA"
    },
    "lover": {
        "bg_gradient": "linear-gradient(135deg, #fff0f5 0%, #fbcfe8 100%)",
        "card_bg": "#ffffff",
        "accent": "#db2777",
        "accent_light": "#fdf2f8",
        "text_color": "#500724",
        "badge_bg": "#fce7f3",
        "badge_text": "#9d174d",
        "shadow": "rgba(219, 39, 119, 0.16)",
        "badge": "💘 LOVER ERA"
    },
    "folklore": {
        "bg_gradient": "linear-gradient(135deg, #fbfbfa 0%, #e7e5e4 100%)",
        "card_bg": "#ffffff",
        "accent": "#57534e",
        "accent_light": "#f5f5f4",
        "text_color": "#1c1917",
        "badge_bg": "#d6d3d1",
        "badge_text": "#292524",
        "shadow": "rgba(87, 83, 78, 0.12)",
        "badge": "🌲 FOLKLORE ERA"
    },
    "evermore": {
        "bg_gradient": "linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%)",
        "card_bg": "#ffffff",
        "accent": "#c2410c",
        "accent_light": "#fffaf5",
        "text_color": "#431407",
        "badge_bg": "#fed7aa",
        "badge_text": "#7c2d12",
        "shadow": "rgba(194, 65, 12, 0.15)",
        "badge": "🍂 EVERMORE ERA"
    },
    "midnights": {
        "bg_gradient": "linear-gradient(135deg, #f5f3ff 0%, #ddd6fe 100%)",
        "card_bg": "#ffffff",
        "accent": "#4338ca",
        "accent_light": "#eef2ff",
        "text_color": "#1e1b4b",
        "badge_bg": "#c7d2fe",
        "badge_text": "#312e81",
        "shadow": "rgba(67, 56, 202, 0.15)",
        "badge": "🌙 MIDNIGHTS ERA"
    },
    "the tortured poets department": {
        "bg_gradient": "linear-gradient(135deg, #fafaf9 0%, #e7e5e4 100%)",
        "card_bg": "#ffffff",
        "accent": "#44403c",
        "accent_light": "#f5f5f4",
        "text_color": "#1c1917",
        "badge_bg": "#e7e5e4",
        "badge_text": "#292524",
        "shadow": "rgba(68, 64, 60, 0.12)",
        "badge": "🖋 TTPD ERA"
    },
    "life of a showgirl": {
        "bg_gradient": "linear-gradient(135deg, #fdf4ff 0%, #f5d0fe 100%)",
        "card_bg": "#ffffff",
        "accent": "#a21caf",
        "accent_light": "#fdf2f8",
        "text_color": "#4a044e",
        "badge_bg": "#f0abfc",
        "badge_text": "#701a75",
        "shadow": "rgba(162, 28, 175, 0.16)",
        "badge": "🎭 SHOWGIRL ERA"
    }
}

DEFAULT_THEME = {
    "bg_gradient": "linear-gradient(135deg, #fff0f5 0%, #ffe4e6 100%)",
    "card_bg": "#ffffff",
    "accent": "#e11d48",
    "accent_light": "#fff1f2",
    "text_color": "#2c151c",
    "badge_bg": "#fecdd3",
    "badge_text": "#881337",
    "shadow": "rgba(225, 29, 72, 0.12)",
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
    st.session_state.album_ratings = {}
    st.session_state.all_song_ratings = {}
    st.session_state.album_winners = []
    st.session_state.lucky_13_count = 0
    st.session_state.current_album = None
    st.session_state.bracket_list = []
    st.session_state.bracket_winner = None
    st.session_state.bracket_step = 1
    st.session_state.final_winner = None


# --- DYNAMIC LIGHT STYLING ---
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
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            transition: background 0.5s ease-in-out;
        }}
        h1, h2, h3, h4, p, label, .stMarkdown {{
            color: {theme['text_color']} !important;
        }}
        .era-card {{
            background-color: {theme['card_bg']};
            border: 1px solid rgba(0, 0, 0, 0.06);
            box-shadow: 0 10px 25px {theme['shadow']};
            border-radius: 18px;
            padding: 24px;
            margin-bottom: 24px;
        }}
        .era-badge {{
            display: inline-block;
            background-color: {theme['badge_bg']};
            color: {theme['badge_text']} !important;
            padding: 6px 14px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
            margin-bottom: 14px;
        }}
        /* Primary Buttons */
        div.stButton > button {{
            background-color: {theme['accent']};
            color: #ffffff !important;
            border: none;
            font-weight: 600;
            font-size: 0.95rem;
            border-radius: 12px;
            padding: 0.65rem 1.4rem;
            box-shadow: 0 4px 12px {theme['shadow']};
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        div.stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 18px {theme['shadow']};
        }}
        /* Sliders */
        div[data-testid="stSlider"] label {{
            font-weight: 600;
            font-size: 1rem;
        }}
    </style>
""", unsafe_allow_html=True)


def trigger_random_easter_egg():
    if random.random() < 0.25:
        egg = random.choice(EGGS)
        st.toast(egg, icon="💎")


# ==============================================================================
# SCREEN 1: ERA SELECTOR
# ==============================================================================
if st.session_state.phase == "SELECT_ALBUM":
    st.session_state.current_album = None

    st.markdown('<div class="era-badge">👑 ERA TOURNAMENT HUB</div>', unsafe_allow_html=True)
    st.title("The Ultimate Taylor Swift Era Bracket")
    st.write(
        "Rate songs across Taylor's discography on a 13-point scale, settle album ties with head-to-head showdowns, and discover your true Swiftie Era personality!")

    remaining_albums = [a for a in all_albums if a not in st.session_state.album_ratings]

    col_main, col_stats = st.columns([2, 1])

    with col_main:
        st.markdown('<div class="era-card">', unsafe_allow_html=True)
        if not remaining_albums:
            st.success("🎉 You've rated every album! The stage is ready for your Final Era Showdown.")
            if st.button("Enter The Ultimate Showdown 🏆", use_container_width=True):
                st.session_state.bracket_list = list(st.session_state.album_winners)
                random.shuffle(st.session_state.bracket_list)
                st.session_state.bracket_winner = st.session_state.bracket_list[0]
                st.session_state.bracket_step = 1
                st.session_state.phase = "FINAL_BRACKET"
                st.rerun()
        else:
            selected = st.selectbox("Choose an Era to rate:", remaining_albums)

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
        st.markdown('</div>', unsafe_allow_html=True)

    with col_stats:
        st.markdown('<div class="era-card">', unsafe_allow_html=True)
        st.subheader("Your Tour Stats")
        st.write(f"**Eras Finished:** {len(st.session_state.album_ratings)} / {len(all_albums)}")
        st.write(f"**Lucky 13s Awarded:** {st.session_state.lucky_13_count} 💎")

        if st.session_state.album_ratings:
            st.divider()
            st.write("**Top Rated Era So Far:**")
            top_era = max(st.session_state.album_ratings, key=st.session_state.album_ratings.get)
            st.write(f"✨ **{top_era}** ({st.session_state.album_ratings[top_era]:.2f}/13)")
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SCREEN 2: RATE SONGS IN CHOSEN ALBUM
# ==============================================================================
elif st.session_state.phase == "RATE_ALBUM":
    album = st.session_state.current_album
    badge_label = ERA_THEMES.get(album.lower(), DEFAULT_THEME)["badge"]

    st.markdown(f'<div class="era-badge">{badge_label}</div>', unsafe_allow_html=True)
    st.title(f"Rating: {album}")
    st.write("Score each track from **1 to 13**. Songs that earn a **13** count toward unlocking **Mastermind Mode**!")

    songs_in_album = songs_df[songs_df['Album'] == album]["Song"].tolist()

    st.markdown('<div class="era-card">', unsafe_allow_html=True)
    with st.form(key="rating_form"):
        ratings = {}
        col1, col2 = st.columns(2)
        for idx, song in enumerate(songs_in_album):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                ratings[song] = st.slider(
                    f"🎵 {song}",
                    min_value=1,
                    max_value=13,
                    value=10,
                    key=f"rating_{song}"
                )
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Lock In Ratings 🔒", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        awarded_13s = sum(1 for score in ratings.values() if score == 13)
        st.session_state.lucky_13_count += awarded_13s
        if awarded_13s > 0:
            st.balloons()
            st.toast(f"💎 Lucky 13! Taylor would approve. (+{awarded_13s} added)", icon="✨")

        st.session_state.all_song_ratings.update(ratings)

        avg_score = sum(ratings.values()) / len(ratings)
        st.session_state.album_ratings[album] = avg_score

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
        st.title("The Grand Finale")
        st.write("The top songs from each of your rated eras face off head-to-head for the crown.")
    else:
        album = st.session_state.current_album
        st.markdown(f'<div class="era-badge">⚡ {album.upper()} TIEBREAKER</div>', unsafe_allow_html=True)
        st.title("Tiebreaker Matchup")
        st.write("Multiple songs share the top score! Choose your favorite to win the album:")

    if step < len(contenders):
        challenger = contenders[step]

        st.markdown('<div class="era-card">', unsafe_allow_html=True)
        st.caption(f"MATCHUP {step} OF {len(contenders) - 1}")

        c1, c_vs, c2 = st.columns([5, 1, 5])

        with c1:
            st.markdown(f"#### 👑 Frontrunner\n### {current_champ}")
            if st.button(f"Vote for '{current_champ}'", key=f"champ_{step}", use_container_width=True):
                trigger_random_easter_egg()
                st.session_state.bracket_step += 1
                st.rerun()

        with c_vs:
            st.markdown("<h2 style='text-align: center; margin-top: 30px; color: #a1a1aa;'>VS</h2>",
                        unsafe_allow_html=True)

        with c2:
            st.markdown(f"#### ⚡ Challenger\n### {challenger}")
            if st.button(f"Vote for '{challenger}'", key=f"chal_{step}", use_container_width=True):
                trigger_random_easter_egg()
                st.session_state.bracket_winner = challenger
                st.session_state.bracket_step += 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        winner = current_champ
        if not is_final:
            st.session_state.album_winners.append(winner)
            st.session_state.phase = "SELECT_ALBUM"
            st.toast(f"Album winner: {winner}! 👑", icon="✨")
            st.rerun()
        else:
            st.session_state.final_winner = winner
            st.session_state.phase = "RESULTS"
            st.rerun()

# ==============================================================================
# SCREEN 4: RESULTS & PERSONALITY
# ==============================================================================
elif st.session_state.phase == "RESULTS":
    st.balloons()
    st.markdown('<div class="era-badge">✨ YOUR ERA HAS BEEN CHOSEN</div>', unsafe_allow_html=True)
    st.title("Your Official Era Results")

    best_album = max(st.session_state.album_ratings, key=st.session_state.album_ratings.get)
    best_score = st.session_state.album_ratings[best_album]
    meta = ALBUM_DATA.get(best_album.lower(), (
        "You have pristine taste across every single album.",
        "Taylor Swift",
        "The Visionary"
    ))

    # Bright Results Card
    st.markdown(f"""
        <div class="era-card">
            <h1 style="color: {theme['accent']} !important; margin-bottom: 5px;">👑 #1 Song: {st.session_state.final_winner}</h1>
            <h3 style="margin-top: 0;">💖 Favorite Era: {best_album} (Avg Score: {best_score:.2f}/13)</h3>
            <p style="font-size: 1.15rem; font-style: italic; margin-top: 15px; line-height: 1.6;">"{meta[0]}"</p>
            <hr style="border: none; border-top: 1px solid #f0f0f0; margin: 20px 0;">
            <p style="font-size: 1.05rem;"><strong>👑 Swiftie Title:</strong> {meta[2]}</p>
            <p style="font-size: 1.05rem;"><strong>🎧 Recommended Artist:</strong> {meta[1]}</p>
        </div>
    """, unsafe_allow_html=True)

    # Mastermind Mode Check
    all_rated = len(st.session_state.album_ratings) == len(all_albums)
    is_mastermind = (st.session_state.lucky_13_count >= 13 and best_score >= 12 and all_rated)

    if is_mastermind:
        st.markdown("""
            <div style="background-color: #ecfdf5; border: 2px solid #10b981; border-radius: 16px; padding: 22px; margin-bottom: 25px;">
                <h2 style="color: #065f46 !important; margin-top: 0;">🧠 MASTERMIND MODE ACTIVATED 🧠</h2>
                <p style="color: #047857 !important; font-size: 1.05rem;">You didn’t just rate songs... You calculated outcomes. You noticed patterns. You played strategically.</p>
                <p style="color: #065f46 !important;"><strong>👑 Swiftie Rank:</strong> The Architect | <strong>💎 Rarity:</strong> Legendary | <strong>🧠 Era Energy:</strong> Mastermind</p>
                <p style="color: #047857 !important; font-style: italic; margin-bottom: 0;">You were never guessing. You were always in control.</p>
            </div>
        """, unsafe_allow_html=True)

    # Top Songs Table & Playlist Export
    st.subheader("Your Ranked Tracklist")
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
            file_name="my_taylor_top_tracks.csv",
            mime="text/csv",
            use_container_width=True
        )
        if st.button("Start Over 🔄", use_container_width=True):
            st.session_state.clear()
            st.rerun()