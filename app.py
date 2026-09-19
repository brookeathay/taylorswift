import streamlit as st
import pandas as pd
import random

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="The Eras Tour Bracket Experience",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- THEMED ERAS METADATA ---
ERA_THEMES = {
    "taylor swift": {
        "bg_gradient": "linear-gradient(135deg, #f2f7ef 0%, #dcecd4 100%)",
        "card_bg": "#ffffff",
        "accent": "#41724d",
        "text_color": "#1f3324",
        "badge_bg": "#c5e1a5",
        "badge_text": "#2e4f19",
        "shadow": "rgba(65, 114, 77, 0.18)",
        "badge": "🌻 DEBUT ERA",
        "icon": "🦋",
        "floating_emojis": ["🦋", "🎸", "🌻", "🤠", "👢", "🍃"],
        "tagline": "Handwritten lyrics, porch swings, and teenage country dreams."
    },
    "fearless": {
        "bg_gradient": "linear-gradient(135deg, #fffdf0 0%, #fae8ad 100%)",
        "card_bg": "#ffffff",
        "accent": "#b8860b",
        "text_color": "#422e03",
        "badge_bg": "#ffe082",
        "badge_text": "#5d4037",
        "shadow": "rgba(184, 134, 11, 0.22)",
        "badge": "✨ FEARLESS (TAYLOR'S VERSION)",
        "icon": "✨",
        "floating_emojis": ["✨", "💛", "👑", "🌧️", "🏰", "🤍"],
        "tagline": "Dancing in the rain with golden butterflies."
    },
    "speak now": {
        "bg_gradient": "linear-gradient(135deg, #faf3ff 0%, #ead0fc 100%)",
        "card_bg": "#ffffff",
        "accent": "#7e22ce",
        "text_color": "#330c4e",
        "badge_bg": "#e9d5ff",
        "badge_text": "#581c87",
        "shadow": "rgba(126, 34, 206, 0.2)",
        "badge": "💜 SPEAK NOW (TAYLOR'S VERSION)",
        "icon": "🐉",
        "floating_emojis": ["💜", "🐉", "🎆", "🏰", "💌", "✨"],
        "tagline": "Sparks flying, fighting dragons, and heartfelt confessions."
    },
    "red": {
        "bg_gradient": "linear-gradient(135deg, #fff3f3 0%, #ffd0d3 100%)",
        "card_bg": "#ffffff",
        "accent": "#be123c",
        "text_color": "#4c0519",
        "badge_bg": "#fecdd3",
        "badge_text": "#881337",
        "shadow": "rgba(190, 18, 60, 0.22)",
        "badge": "🧣 RED (TAYLOR'S VERSION)",
        "icon": "🧣",
        "floating_emojis": ["🧣", "🍁", "🍷", "🍂", "💔", "🕶️"],
        "tagline": "Passionate, burning, nostalgic, and beautifully chaotic."
    },
    "1989": {
        "bg_gradient": "linear-gradient(135deg, #f0f9ff 0%, #bee3f8 100%)",
        "card_bg": "#ffffff",
        "accent": "#0284c7",
        "text_color": "#082f49",
        "badge_bg": "#bae6fd",
        "badge_text": "#0369a1",
        "shadow": "rgba(2, 132, 199, 0.2)",
        "badge": "🕶 1989 (TAYLOR'S VERSION)",
        "icon": "🩵",
        "floating_emojis": ["🩵", "🪩", "🕶️", "🏙️", "🌊", "🕊️"],
        "tagline": "Polaroids, skyline views, and unapologetic pop perfection."
    },
    "reputation": {
        "bg_gradient": "linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%)",
        "card_bg": "#ffffff",
        "accent": "#0f172a",
        "text_color": "#020617",
        "badge_bg": "#0f172a",
        "badge_text": "#f8fafc",
        "shadow": "rgba(15, 23, 42, 0.25)",
        "badge": "🐍 REPUTATION ERA",
        "icon": "🐍",
        "floating_emojis": ["🐍", "🖤", "📰", "⛓️", "🗝️", "🍸"],
        "tagline": "Big reputations, dark alleys, and fiercely guarded true love."
    },
    "lover": {
        "bg_gradient": "linear-gradient(135deg, #fff0f6 0%, #fbcfe8 100%)",
        "card_bg": "#ffffff",
        "accent": "#db2777",
        "text_color": "#500724",
        "badge_bg": "#fce7f3",
        "badge_text": "#9d174d",
        "shadow": "rgba(219, 39, 119, 0.2)",
        "badge": "💘 LOVER ERA",
        "icon": "💖",
        "floating_emojis": ["💖", "💘", "🌈", "🌸", "🏹", "🍭"],
        "tagline": "Pastel cotton candy skies, heart sunglasses, and hopeless romance."
    },
    "folklore": {
        "bg_gradient": "linear-gradient(135deg, #fafaf9 0%, #e7e5e4 100%)",
        "card_bg": "#ffffff",
        "accent": "#57534e",
        "text_color": "#1c1917",
        "badge_bg": "#e7e5e4",
        "badge_text": "#292524",
        "shadow": "rgba(87, 83, 78, 0.16)",
        "badge": "🌲 FOLKLORE ERA",
        "icon": "🕯️",
        "floating_emojis": ["🕯️", "🌲", "🧶", "🪞", "🩶", "📜"],
        "tagline": "Whispering pine trees, old cardigans, and untold secrets."
    },
    "evermore": {
        "bg_gradient": "linear-gradient(135deg, #fff7ed 0%, #fed7aa 100%)",
        "card_bg": "#ffffff",
        "accent": "#c2410c",
        "text_color": "#431407",
        "badge_bg": "#ffedd5",
        "badge_text": "#7c2d12",
        "shadow": "rgba(194, 65, 12, 0.2)",
        "badge": "🍂 EVERMORE ERA",
        "icon": "🌲",
        "floating_emojis": ["🍂", "🪵", "☕", "🍷", "🤎", "❄️"],
        "tagline": "Cabin fires, willow branches, and poetic winter mysteries."
    },
    "midnights": {
        "bg_gradient": "linear-gradient(135deg, #f5f3ff 0%, #c7d2fe 100%)",
        "card_bg": "#ffffff",
        "accent": "#4338ca",
        "text_color": "#1e1b4b",
        "badge_bg": "#e0e7ff",
        "badge_text": "#312e81",
        "shadow": "rgba(67, 56, 202, 0.22)",
        "badge": "🌙 MIDNIGHTS ERA",
        "icon": "🌙",
        "floating_emojis": ["🌙", "💎", "🕰️", "🪩", "🌌", "🕯️"],
        "tagline": "Meet me at midnight: sleepless nights, lavender haze, and clockwork."
    },
    "the tortured poets department": {
        "bg_gradient": "linear-gradient(135deg, #fbfbfa 0%, #d6d3d1 100%)",
        "card_bg": "#ffffff",
        "accent": "#44403c",
        "text_color": "#1c1917",
        "badge_bg": "#e7e5e4",
        "badge_text": "#1c1917",
        "shadow": "rgba(68, 64, 60, 0.18)",
        "badge": "🖋 THE TORTURED POETS DEPARTMENT",
        "icon": "🖋️",
        "floating_emojis": ["🖋️", "📜", "📖", "⏳", "🤍", "☕"],
        "tagline": "Typewriters, statues, manuscript margins, and manic melancholia."
    },
    "life of a showgirl": {
        "bg_gradient": "linear-gradient(135deg, #fdf4ff 0%, #f0abfc 100%)",
        "card_bg": "#ffffff",
        "accent": "#9333ea",
        "text_color": "#4a044e",
        "badge_bg": "#fae8ff",
        "badge_text": "#701a75",
        "shadow": "rgba(147, 51, 234, 0.22)",
        "badge": "🎭 SHOWGIRL ERA",
        "icon": "🎭",
        "floating_emojis": ["🎭", "💄", "🪞", "✨", "🎟️", "🥂"],
        "tagline": "Glittering stage lights, heavy velvet curtains, and raw drama."
    }
}

DEFAULT_THEME = {
    "bg_gradient": "linear-gradient(135deg, #fff1f2 0%, #fecdd3 100%)",
    "card_bg": "#ffffff",
    "accent": "#e11d48",
    "text_color": "#3f0a1c",
    "badge_bg": "#ffe4e6",
    "badge_text": "#9f1239",
    "shadow": "rgba(225, 29, 72, 0.18)",
    "badge": "👑 THE ERAS TOUR",
    "icon": "✨",
    "floating_emojis": ["✨", "👑", "🪩", "💖", "🐍", "🧣"],
    "tagline": "Journey across all 11+ musical eras in one comprehensive tournament."
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


# --- LOAD SONGS ---
@st.cache_data
def load_songs():
    try:
        return pd.read_csv("songs.csv")
    except FileNotFoundError:
        st.error("⚠️ `songs.csv` not found in current folder.")
        st.stop()


songs_df = load_songs()
all_albums = list(songs_df['Album'].unique())

# --- SESSION STATE ---
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


def get_current_theme():
    if st.session_state.current_album:
        return ERA_THEMES.get(st.session_state.current_album.lower(), DEFAULT_THEME)
    return DEFAULT_THEME


theme = get_current_theme()

# --- ANIMATED FLOATING SYMBOLS CSS ---
floating_html = "".join([
    f'<span class="floating-symbol symbol-{i}">{emoji}</span>'
    for i, emoji in enumerate(theme["floating_emojis"])
])

st.markdown(f"""
    <style>
        .stApp {{
            background: {theme['bg_gradient']};
            color: {theme['text_color']};
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            overflow-x: hidden;
            transition: background 0.7s ease;
        }}

        /* Floating Emoji Animations */
        .ambient-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }}
        .floating-symbol {{
            position: absolute;
            font-size: 2.4rem;
            opacity: 0.22;
            animation: floatUpDown 8s ease-in-out infinite alternate;
        }}
        .symbol-0 {{ top: 12%; left: 8%; animation-duration: 7s; }}
        .symbol-1 {{ top: 70%; left: 12%; animation-duration: 9s; font-size: 3rem; }}
        .symbol-2 {{ top: 25%; right: 10%; animation-duration: 8.5s; }}
        .symbol-3 {{ top: 80%; right: 15%; animation-duration: 10s; font-size: 2.8rem; }}
        .symbol-4 {{ top: 50%; left: 88%; animation-duration: 6.5s; }}
        .symbol-5 {{ top: 88%; left: 45%; animation-duration: 11s; font-size: 2.2rem; }}

        @keyframes floatUpDown {{
            0% {{ transform: translateY(0px) rotate(0deg) scale(1); }}
            50% {{ transform: translateY(-30px) rotate(12deg) scale(1.1); }}
            100% {{ transform: translateY(20px) rotate(-10deg) scale(0.95); }}
        }}

        /* Visual Cards */
        .era-card {{
            position: relative;
            z-index: 1;
            background-color: {theme['card_bg']};
            border: 1.5px solid rgba(0, 0, 0, 0.05);
            box-shadow: 0 12px 35px {theme['shadow']};
            border-radius: 20px;
            padding: 26px;
            margin-bottom: 24px;
        }}

        .era-hero {{
            position: relative;
            z-index: 1;
            background: linear-gradient(135deg, #ffffff 0%, rgba(255, 255, 255, 0.75) 100%);
            border: 2px solid {theme['accent']};
            box-shadow: 0 14px 40px {theme['shadow']};
            border-radius: 22px;
            padding: 30px;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 22px;
        }}

        .hero-icon {{
            font-size: 4rem;
            animation: pulseGlow 2.5s ease-in-out infinite alternate;
        }}

        @keyframes pulseGlow {{
            0% {{ transform: scale(1); filter: drop-shadow(0 0 2px rgba(0,0,0,0.1)); }}
            100% {{ transform: scale(1.1); filter: drop-shadow(0 0 14px {theme['accent']}); }}
        }}

        .era-badge {{
            display: inline-block;
            background-color: {theme['badge_bg']};
            color: {theme['badge_text']} !important;
            padding: 7px 16px;
            border-radius: 999px;
            font-weight: 800;
            font-size: 0.85rem;
            letter-spacing: 0.8px;
            margin-bottom: 12px;
        }}

        /* Buttons & Interactive Elements */
        div.stButton > button {{
            background-color: {theme['accent']};
            color: #ffffff !important;
            border: none;
            font-weight: 700;
            font-size: 1rem;
            border-radius: 12px;
            padding: 0.7rem 1.4rem;
            box-shadow: 0 5px 15px {theme['shadow']};
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        div.stButton > button:hover {{
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 10px 22px {theme['shadow']};
        }}
    </style>
    <div class="ambient-container">
        {floating_html}
    </div>
""", unsafe_allow_html=True)


def trigger_random_easter_egg():
    if random.random() < 0.25:
        egg = random.choice(EGGS)
        st.toast(egg, icon="💎")


# ==============================================================================
# SCREEN 1: ERA HUB
# ==============================================================================
if st.session_state.phase == "SELECT_ALBUM":
    st.session_state.current_album = None

    st.markdown(f"""
        <div class="era-hero">
            <div class="hero-icon">{theme['icon']}</div>
            <div>
                <div class="era-badge">👑 ERA TOURNAMENT ARENA</div>
                <h1 style="margin: 0; font-size: 2.2rem; color: {theme['text_color']};">The Eras Tour Bracket</h1>
                <p style="margin: 6px 0 0 0; font-size: 1.05rem; opacity: 0.85;">{theme['tagline']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    remaining_albums = [a for a in all_albums if a not in st.session_state.album_ratings]
    c_main, c_stats = st.columns([2, 1])

    with c_main:
        st.markdown('<div class="era-card">', unsafe_allow_html=True)
        if not remaining_albums:
            st.success("🎉 You have rated every single album! Ready for the Grand Finale Showdown?")
            if st.button("Enter The Ultimate Showdown 🏆", use_container_width=True):
                st.session_state.bracket_list = list(st.session_state.album_winners)
                random.shuffle(st.session_state.bracket_list)
                st.session_state.bracket_winner = st.session_state.bracket_list[0]
                st.session_state.bracket_step = 1
                st.session_state.phase = "FINAL_BRACKET"
                st.rerun()
        else:
            selected = st.selectbox(
                "Select an Era to dive into:",
                remaining_albums,
                format_func=lambda x: f"{ERA_THEMES.get(x.lower(), DEFAULT_THEME)['icon']} {x}"
            )

            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"Rate Era 🎵", use_container_width=True):
                    trigger_random_easter_egg()
                    st.session_state.current_album = selected
                    st.session_state.phase = "RATE_ALBUM"
                    st.rerun()
            with c2:
                if st.session_state.album_winners:
                    if st.button("Jump to Finals 🏆", use_container_width=True):
                        st.session_state.bracket_list = list(st.session_state.album_winners)
                        random.shuffle(st.session_state.bracket_list)
                        st.session_state.bracket_winner = st.session_state.bracket_list[0]
                        st.session_state.bracket_step = 1
                        st.session_state.phase = "FINAL_BRACKET"
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c_stats:
        st.markdown('<div class="era-card">', unsafe_allow_html=True)
        st.subheader("Your Tour Stats")
        st.write(f"**Completed Eras:** {len(st.session_state.album_ratings)} / {len(all_albums)}")
        st.write(f"**Lucky 13s Found:** {st.session_state.lucky_13_count} 💎")

        if st.session_state.album_ratings:
            st.divider()
            st.write("**Current Favorite Era:**")
            top_era = max(st.session_state.album_ratings, key=st.session_state.album_ratings.get)
            top_meta = ERA_THEMES.get(top_era.lower(), DEFAULT_THEME)
            st.write(f"{top_meta['icon']} **{top_era}** ({st.session_state.album_ratings[top_era]:.2f}/13)")
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SCREEN 2: RATE SONGS IN CURRENT ERA
# ==============================================================================
elif st.session_state.phase == "RATE_ALBUM":
    album = st.session_state.current_album
    meta = ERA_THEMES.get(album.lower(), DEFAULT_THEME)

    st.markdown(f"""
        <div class="era-hero">
            <div class="hero-icon">{meta['icon']}</div>
            <div>
                <div class="era-badge">{meta['badge']}</div>
                <h1 style="margin: 0; font-size: 2.2rem; color: {theme['text_color']};">{album}</h1>
                <p style="margin: 6px 0 0 0; font-size: 1.05rem; opacity: 0.85;">{meta['tagline']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    songs_in_album = songs_df[songs_df['Album'] == album]["Song"].tolist()

    st.markdown('<div class="era-card">', unsafe_allow_html=True)
    with st.form(key="rating_form"):
        ratings = {}
        col1, col2 = st.columns(2)
        for idx, song in enumerate(songs_in_album):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                ratings[song] = st.slider(
                    f"{meta['icon']} {song}",
                    min_value=1,
                    max_value=13,
                    value=10,
                    key=f"song_{song}"
                )
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Lock In Era Ratings 🔒", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        awarded_13s = sum(1 for score in ratings.values() if score == 13)
        st.session_state.lucky_13_count += awarded_13s
        if awarded_13s > 0:
            st.balloons()
            st.toast(f"💎 Lucky 13! Taylor would approve. (+{awarded_13s} logged)", icon="✨")

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
# SCREEN 3: INTERACTIVE SHOWDOWN ARENA
# ==============================================================================
elif st.session_state.phase in ["ALBUM_TIEBREAKER", "FINAL_BRACKET"]:
    is_final = (st.session_state.phase == "FINAL_BRACKET")
    contenders = st.session_state.bracket_list
    current_champ = st.session_state.bracket_winner
    step = st.session_state.bracket_step

    title_badge = "🏆 ULTIMATE ERA SHOWDOWN" if is_final else f"⚡ {st.session_state.current_album.upper()} TIEBREAKER"
    subtitle = "The #1 tracks across your rated eras go head-to-head for the crown." if is_final else "A tie occurred! Select which track advances:"

    st.markdown(f"""
        <div class="era-hero">
            <div class="hero-icon">⚔️</div>
            <div>
                <div class="era-badge">{title_badge}</div>
                <h1 style="margin: 0; font-size: 2.2rem; color: {theme['text_color']};">The Arena Showdown</h1>
                <p style="margin: 6px 0 0 0; font-size: 1.05rem; opacity: 0.85;">{subtitle}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if step < len(contenders):
        challenger = contenders[step]

        st.markdown('<div class="era-card">', unsafe_allow_html=True)
        st.caption(f"MATCHUP ROUND {step} OF {len(contenders) - 1}")

        c1, c_vs, c2 = st.columns([5, 1, 5])

        with c1:
            st.markdown(f"#### 👑 Frontrunner\n### {current_champ}")
            if st.button(f"Vote '{current_champ}'", key=f"champ_{step}", use_container_width=True):
                trigger_random_easter_egg()
                st.session_state.bracket_step += 1
                st.rerun()

        with c_vs:
            st.markdown(f"""
                <div style="text-align: center; margin-top: 30px;">
                    <span style="background: {theme['accent']}; color: #fff; padding: 6px 12px; border-radius: 999px; font-weight: 800; font-size: 0.9rem;">
                        VS
                    </span>
                </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"#### ⚡ Challenger\n### {challenger}")
            if st.button(f"Vote '{challenger}'", key=f"chal_{step}", use_container_width=True):
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
            st.toast(f"Winner declared: {winner}! 👑", icon="✨")
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
    best_album = max(st.session_state.album_ratings, key=st.session_state.album_ratings.get)
    best_score = st.session_state.album_ratings[best_album]
    best_meta = ERA_THEMES.get(best_album.lower(), DEFAULT_THEME)

    st.markdown(f"""
        <div class="era-hero">
            <div class="hero-icon">{best_meta['icon']}</div>
            <div>
                <div class="era-badge">✨ YOUR ERA HAS BEEN CHOSEN</div>
                <h1 style="margin: 0; font-size: 2.2rem; color: {theme['text_color']};">The Crown Goes To {best_album}</h1>
                <p style="margin: 6px 0 0 0; font-size: 1.05rem; opacity: 0.85;">{best_meta['tagline']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    meta = ALBUM_DATA.get(best_album.lower(), (
        "You have elite taste across every single era.",
        "Taylor Swift",
        "The Visionary"
    ))

    st.markdown(f"""
        <div class="era-card">
            <h1 style="color: {best_meta['accent']} !important; margin-bottom: 5px;">👑 #1 Overall Song: {st.session_state.final_winner}</h1>
            <h3 style="margin-top: 0;">💖 Favorite Era: {best_album} (Avg Score: {best_score:.2f}/13)</h3>
            <p style="font-size: 1.15rem; font-style: italic; margin-top: 15px; line-height: 1.6;">"{meta[0]}"</p>
            <hr style="border: none; border-top: 1px solid #f0f0f0; margin: 20px 0;">
            <p style="font-size: 1.05rem;"><strong>👑 Swiftie Title:</strong> {meta[2]}</p>
            <p style="font-size: 1.05rem;"><strong>🎧 Recommended Artist:</strong> {meta[1]}</p>
        </div>
    """, unsafe_allow_html=True)

    # Mastermind Mode
    all_rated = len(st.session_state.album_ratings) == len(all_albums)
    is_mastermind = (st.session_state.lucky_13_count >= 13 and best_score >= 12 and all_rated)

    if is_mastermind:
        st.markdown("""
            <div style="background-color: #f0fdf4; border: 2px solid #16a34a; border-radius: 18px; padding: 24px; margin-bottom: 25px;">
                <h2 style="color: #15803d !important; margin-top: 0;">🧠 MASTERMIND MODE ACTIVATED 🧠</h2>
                <p style="color: #166534 !important; font-size: 1.05rem;">You didn’t just rate songs... You calculated outcomes. You noticed patterns. You played strategically.</p>
                <p style="color: #15803d !important;"><strong>👑 Swiftie Rank:</strong> The Architect | <strong>💎 Rarity:</strong> Legendary | <strong>🧠 Era Energy:</strong> Mastermind</p>
                <p style="color: #166534 !important; font-style: italic; margin-bottom: 0;">You were never guessing. You were always in control.</p>
            </div>
        """, unsafe_allow_html=True)

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