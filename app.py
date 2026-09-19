import streamlit as st
import pandas as pd
import random

# --- PAGE SETUP ---
st.set_page_config(
    page_title="The Eras Tour Bracket & Festival",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ERA METADATA & PALETTES ---
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
        "floating_emojis": ["🦋", "🎸", "🌻", "🤠", "👢"],
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
        "badge": "✨ FEARLESS (TV)",
        "icon": "✨",
        "floating_emojis": ["✨", "💛", "👑", "🌧️", "🤍"],
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
        "badge": "💜 SPEAK NOW (TV)",
        "icon": "🐉",
        "floating_emojis": ["💜", "🐉", "🎆", "🏰", "💌"],
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
        "badge": "🧣 RED (TV)",
        "icon": "🧣",
        "floating_emojis": ["🧣", "🍁", "🍷", "🍂", "💔"],
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
        "badge": "🕶 1989 (TV)",
        "icon": "🩵",
        "floating_emojis": ["🩵", "🪩", "🕶️", "🏙️", "🌊"],
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
        "badge": "🐍 REPUTATION",
        "icon": "🐍",
        "floating_emojis": ["🐍", "🖤", "📰", "⛓️", "🍸"],
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
        "badge": "💘 LOVER",
        "icon": "💖",
        "floating_emojis": ["💖", "💘", "🌈", "🌸", "🏹"],
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
        "badge": "🌲 FOLKLORE",
        "icon": "🕯️",
        "floating_emojis": ["🕯️", "🌲", "🧶", "🪞", "🩶"],
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
        "badge": "🍂 EVERMORE",
        "icon": "🌲",
        "floating_emojis": ["🍂", "🪵", "☕", "🍷", "🤎"],
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
        "badge": "🌙 MIDNIGHTS",
        "icon": "🌙",
        "floating_emojis": ["🌙", "💎", "🕰️", "🪩", "🌌"],
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
        "badge": "🖋 TTPD",
        "icon": "🖋️",
        "floating_emojis": ["🖋️", "📜", "📖", "⏳", "🤍"],
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
        "badge": "🎭 SHOWGIRL",
        "icon": "🎭",
        "floating_emojis": ["🎭", "💄", "🪞", "✨", "🎟️"],
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
    "floating_emojis": ["✨", "👑", "🪩", "💖", "🧣"],
    "tagline": "The grand tournament across all eras of Taylor Swift's musical journey."
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


# --- AUDIO & CSS INJECTION ---
def play_sound(sound_type="click"):
    # Synthesized Web Audio API sound cues
    freq = 520 if sound_type == "click" else 780
    st.components.v1.html(f"""
        <script>
            try {{
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime({freq}, ctx.currentTime);
                gain.gain.setValueAtTime(0.08, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.18);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.18);
            }} catch(e) {{}}
        </script>
    """, height=0, width=0)


def render_friendship_bracelet(text):
    clean_text = "".join([c for c in text.upper() if c.isalnum() or c == " "])[:22]
    bead_colors = ["#fbcfe8", "#fde047", "#bae6fd", "#bbf7d0", "#ddd6fe", "#fed7aa"]
    beads_html = []
    for i, char in enumerate(clean_text):
        if char == " ":
            beads_html.append('<div class="spacer-bead"></div>')
        else:
            color = bead_colors[i % len(bead_colors)]
            beads_html.append(f'<div class="bracelet-bead" style="background:{color};">{char}</div>')
    return f"""
        <div class="bracelet-container">
            <div class="bracelet-string"></div>
            <div class="beads-row">{''.join(beads_html)}</div>
        </div>
    """


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

        /* Floating Symbols */
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
            font-size: 2.2rem;
            opacity: 0.2;
            animation: floatAnim 8s ease-in-out infinite alternate;
        }}
        .symbol-0 {{ top: 12%; left: 8%; animation-duration: 7s; }}
        .symbol-1 {{ top: 72%; left: 10%; animation-duration: 9s; font-size: 2.8rem; }}
        .symbol-2 {{ top: 22%; right: 12%; animation-duration: 8.5s; }}
        .symbol-3 {{ top: 82%; right: 14%; animation-duration: 10s; font-size: 2.6rem; }}
        .symbol-4 {{ top: 52%; left: 88%; animation-duration: 6.5s; }}
        @keyframes floatAnim {{
            0% {{ transform: translateY(0px) rotate(0deg); }}
            100% {{ transform: translateY(-28px) rotate(14deg); }}
        }}

        /* Hero Banner */
        .era-hero {{
            position: relative;
            z-index: 1;
            background: linear-gradient(135deg, #ffffff 0%, rgba(255, 255, 255, 0.8) 100%);
            border: 2px solid {theme['accent']};
            box-shadow: 0 14px 40px {theme['shadow']};
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        .hero-icon {{
            font-size: 3.6rem;
            animation: pulseIcon 2.5s ease-in-out infinite alternate;
        }}
        @keyframes pulseIcon {{
            0% {{ transform: scale(1); }}
            100% {{ transform: scale(1.12); filter: drop-shadow(0 0 12px {theme['accent']}); }}
        }}

        .era-badge {{
            display: inline-block;
            background-color: {theme['badge_bg']};
            color: {theme['badge_text']} !important;
            padding: 6px 14px;
            border-radius: 999px;
            font-weight: 800;
            font-size: 0.8rem;
            letter-spacing: 0.8px;
            margin-bottom: 8px;
        }}

        .era-card {{
            position: relative;
            z-index: 1;
            background-color: {theme['card_bg']};
            border: 1.5px solid rgba(0, 0, 0, 0.06);
            box-shadow: 0 12px 30px {theme['shadow']};
            border-radius: 18px;
            padding: 22px;
            margin-bottom: 20px;
        }}

        /* Friendship Bracelet Visualizer */
        .bracelet-container {{
            position: relative;
            padding: 26px 0;
            margin: 15px 0 25px 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .bracelet-string {{
            position: absolute;
            width: 100%;
            height: 4px;
            background: #d4d4d8;
            border-radius: 2px;
            z-index: 1;
        }}
        .beads-row {{
            position: relative;
            z-index: 2;
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            justify-content: center;
            max-width: 90%;
        }}
        .bracelet-bead {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 0.85rem;
            color: #18181b;
            border: 2px solid #52525b;
            box-shadow: 0 4px 8px rgba(0,0,0,0.12);
        }}
        .spacer-bead {{
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #a1a1aa;
            margin: 11px 4px;
        }}

        /* Festival Poster Styling */
        .festival-poster {{
            background: #ffffff;
            border: 3px solid {theme['accent']};
            border-radius: 20px;
            padding: 35px 25px;
            text-align: center;
            box-shadow: 0 18px 45px {theme['shadow']};
            margin-bottom: 25px;
        }}

        /* Buttons */
        div.stButton > button {{
            background-color: {theme['accent']};
            color: #ffffff !important;
            border: none;
            font-weight: 700;
            font-size: 0.95rem;
            border-radius: 12px;
            padding: 0.65rem 1.4rem;
            box-shadow: 0 4px 14px {theme['shadow']};
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        div.stButton > button:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 20px {theme['shadow']};
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
# SCREEN 1: ERA HUB & ALBUM CARD GRID
# ==============================================================================
if st.session_state.phase == "SELECT_ALBUM":
    st.session_state.current_album = None

    st.markdown(f"""
        <div class="era-hero">
            <div class="hero-icon">{theme['icon']}</div>
            <div>
                <div class="era-badge">👑 ERA TOURNAMENT ARENA</div>
                <h1 style="margin: 0; font-size: 2.2rem; color: {theme['text_color']};">The Eras Tour Bracket</h1>
                <p style="margin: 4px 0 0 0; font-size: 1rem; opacity: 0.85;">{theme['tagline']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    remaining_albums = [a for a in all_albums if a not in st.session_state.album_ratings]

    # Progress Bar
    completed_ratio = len(st.session_state.album_ratings) / len(all_albums)
    st.progress(completed_ratio,
                text=f"Tour Progress: {len(st.session_state.album_ratings)} of {len(all_albums)} Eras Ranked")

    st.write("### Choose an Era to Enter")

    # Visual Album Cards Grid (3 columns)
    grid_cols = st.columns(3)
    for idx, alb in enumerate(all_albums):
        c = grid_cols[idx % 3]
        meta = ERA_THEMES.get(alb.lower(), DEFAULT_THEME)
        is_done = alb in st.session_state.album_ratings

        with c:
            st.markdown(f"""
                <div style="background:{meta['card_bg']}; border-radius:14px; border:2px solid {meta['accent'] if not is_done else '#94a3b8'}; padding:16px; margin-bottom:12px; box-shadow: 0 4px 12px {meta['shadow']};">
                    <div style="font-size: 2rem;">{meta['icon']}</div>
                    <div style="font-weight: 800; font-size: 1.1rem; color:{meta['text_color']}; margin: 4px 0;">{alb}</div>
                    <div style="font-size: 0.85rem; color:{meta['text_color']}; opacity: 0.85;">
                        {'✅ Score: ' + str(round(st.session_state.album_ratings[alb], 2)) + '/13' if is_done else meta['tagline']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if not is_done:
                if st.button(f"Rate {alb}", key=f"btn_alb_{idx}", use_container_width=True):
                    play_sound("click")
                    trigger_random_easter_egg()
                    st.session_state.current_album = alb
                    st.session_state.phase = "RATE_ALBUM"
                    st.rerun()

    if st.session_state.album_winners:
        st.divider()
        if st.button("🏆 Final Eras Showdown (Start Now)", use_container_width=True):
            play_sound("fanfare")
            st.session_state.bracket_list = list(st.session_state.album_winners)
            random.shuffle(st.session_state.bracket_list)
            st.session_state.bracket_winner = st.session_state.bracket_list[0]
            st.session_state.bracket_step = 1
            st.session_state.phase = "FINAL_BRACKET"
            st.rerun()

# ==============================================================================
# SCREEN 2: RATE SONGS IN CHOSEN ALBUM
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
                <p style="margin: 4px 0 0 0; font-size: 1rem; opacity: 0.85;">{meta['tagline']}</p>
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
        play_sound("click")
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
    subtitle = "The #1 tracks across your rated eras go head-to-head." if is_final else "A tie occurred! Select which track advances:"

    st.markdown(f"""
        <div class="era-hero">
            <div class="hero-icon">⚔️</div>
            <div>
                <div class="era-badge">{title_badge}</div>
                <h1 style="margin: 0; font-size: 2.2rem; color: {theme['text_color']};">Head-to-Head Arena</h1>
                <p style="margin: 4px 0 0 0; font-size: 1rem; opacity: 0.85;">{subtitle}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if step < len(contenders):
        challenger = contenders[step]

        # Tournament Matchup Progress
        progress_val = step / (len(contenders) - 1)
        st.progress(progress_val, text=f"Matchup {step} of {len(contenders) - 1}")

        st.markdown('<div class="era-card">', unsafe_allow_html=True)
        c1, c_vs, c2 = st.columns([5, 1, 5])

        with c1:
            st.markdown(f"#### 👑 Frontrunner\n### {current_champ}")
            if st.button(f"Vote '{current_champ}'", key=f"champ_{step}", use_container_width=True):
                play_sound("click")
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
                play_sound("click")
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
            st.toast(f"Winner: {winner}! 👑", icon="✨")
            st.rerun()
        else:
            st.session_state.final_winner = winner
            st.session_state.phase = "RESULTS"
            st.rerun()

# ==============================================================================
# SCREEN 4: RESULTS, BRACELET & FESTIVAL POSTER
# ==============================================================================
elif st.session_state.phase == "RESULTS":
    st.balloons()
    play_sound("fanfare")
    best_album = max(st.session_state.album_ratings, key=st.session_state.album_ratings.get)
    best_score = st.session_state.album_ratings[best_album]
    best_meta = ERA_THEMES.get(best_album.lower(), DEFAULT_THEME)

    st.markdown(f"""
        <div class="era-hero">
            <div class="hero-icon">{best_meta['icon']}</div>
            <div>
                <div class="era-badge">✨ YOUR ERA HAS BEEN CHOSEN</div>
                <h1 style="margin: 0; font-size: 2.2rem; color: {theme['text_color']};">The Winner: {best_album}</h1>
                <p style="margin: 4px 0 0 0; font-size: 1rem; opacity: 0.85;">{best_meta['tagline']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Friendship Bracelet
    st.write("### 📿 Your Official Friendship Bracelet")
    st.markdown(render_friendship_bracelet(st.session_state.final_winner), unsafe_allow_html=True)

    sorted_songs = sorted(st.session_state.all_song_ratings.items(), key=lambda x: x[1], reverse=True)
    top_headliner = st.session_state.final_winner
    direct_support = [s[0] for s in sorted_songs if s[0] != top_headliner][:4]
    undercard = [s[0] for s in sorted_songs if s[0] not in [top_headliner] + direct_support][:15]

    # The Eras Festival Lineup Poster
    st.markdown(f"""
        <div class="festival-poster">
            <div class="era-badge">🎪 THE ERAS MUSIC FESTIVAL 🎪</div>
            <h4 style="margin: 0; text-transform: uppercase; letter-spacing: 2px; color: #71717a;">Headliner</h4>
            <h1 style="font-size: 3rem; margin: 5px 0 15px 0; color: {best_meta['accent']};">{top_headliner}</h1>
            <hr style="border: none; border-top: 2px dashed #e4e4e7; margin: 15px 0;">
            <h4 style="margin: 0; text-transform: uppercase; letter-spacing: 2px; color: #71717a;">Direct Support</h4>
            <h3 style="margin: 8px 0; color: #27272a;">{' • '.join(direct_support)}</h3>
            <hr style="border: none; border-top: 1px solid #f4f4f5; margin: 15px 0;">
            <p style="font-size: 0.95rem; color: #52525b; line-height: 1.8;">{' • '.join(undercard)}</p>
        </div>
    """, unsafe_allow_html=True)

    # Mastermind Check
    all_rated = len(st.session_state.album_ratings) == len(all_albums)
    is_mastermind = (st.session_state.lucky_13_count >= 13 and best_score >= 12 and all_rated)
    if is_mastermind:
        st.markdown("""
            <div style="background-color: #f0fdf4; border: 2px solid #16a34a; border-radius: 18px; padding: 22px; margin-bottom: 22px;">
                <h2 style="color: #15803d !important; margin-top: 0;">🧠 MASTERMIND MODE ACTIVATED 🧠</h2>
                <p style="color: #166534 !important;">You didn’t just rate songs... You calculated outcomes. You noticed patterns. You played strategically.</p>
                <p style="color: #15803d !important;"><strong>👑 Swiftie Rank:</strong> The Architect | <strong>💎 Rarity:</strong> Legendary</p>
            </div>
        """, unsafe_allow_html=True)

    # Table & Download
    export_df = pd.DataFrame(sorted_songs[:50], columns=["Song", "Rating"])
    col_tbl, col_dl = st.columns([3, 1])
    with col_tbl:
        st.dataframe(export_df, use_container_width=True, hide_index=True)
    with col_dl:
        csv_data = export_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Top 50 CSV",
            data=csv_data,
            file_name="my_eras_tour_playlist.csv",
            mime="text/csv",
            use_container_width=True
        )
        if st.button("Start Fresh 🔄", use_container_width=True):
            st.session_state.clear()
            st.rerun()