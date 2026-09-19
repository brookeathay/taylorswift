import streamlit as st
import pandas as pd
import random
import urllib.parse
import urllib.request
import json

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="The Eras Tour: Ultimate Arena",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- REPUTATION TRACK 5S & SEED DATA ---
TRACK_5_SONGS = [
    ("Cold as You", "Taylor Swift"),
    ("White Horse", "Fearless"),
    ("Dear John", "Speak Now"),
    ("All Too Well", "Red"),
    ("All You Had to Do Was Stay", "1989"),
    ("Delicate", "Reputation"),
    ("The Archer", "Lover"),
    ("My Tears Ricochet", "Folklore"),
    ("Tolerate It", "Evermore"),
    ("You're On Your Own, Kid", "Midnights"),
    ("So Long, London", "The Tortured Poets Department")
]

SPEED_RUN_POOL = [
    "Cruel Summer", "Blank Space", "All Too Well (10 Minute Version)",
    "Anti-Hero", "Love Story", "Style", "August", "Cardigan",
    "Don't Blame Me", "Enchanted", "Karma", "Getaway Car",
    "Willow", "Champagne Problems", "Fortnight", "Down Bad"
]

SWIFT_LYRICS = [
    ("✨ 'Cause darling, I'm a nightmare dressed like a daydream.", "Blank Space (1989)"),
    ("🧣 And you call me up again just to break me like a promise.", "All Too Well (Red)"),
    ("💎 Best believe I'm still bejeweled, when I walk in the room I can still make the whole place shimmer.",
     "Bejeweled (Midnights)"),
    ("🌲 Are there still beautiful things? Sweet tea in the summer, cross your heart.", "Seven (Folklore)"),
    ("🐍 Honey, I rose up from the dead, I do it all the time.", "Look What You Made Me Do (Reputation)"),
    ("💘 I've loved you three summers now, honey, but I want 'em all.", "Lover (Lover)"),
    ("💜 Long live all the magic we made, and bring on all the pretenders.", "Long Live (Speak Now)"),
    ("🍂 Long story short, I survived.", "Long Story Short (Evermore)"),
    ("🖋️ You're not Dylan Thomas, I'm not Patti Smith. We're modern idiots.", "TTPD")
]

ERA_THEMES = {
    "taylor swift": {
        "bg_gradient": "linear-gradient(135deg, #f2f7ef 0%, #dcecd4 100%)",
        "card_bg": "#ffffff",
        "accent": "#41724d",
        "wristband": "#4ade80",
        "text_color": "#1f3324",
        "badge_bg": "#c5e1a5",
        "badge_text": "#2e4f19",
        "shadow": "rgba(65, 114, 77, 0.18)",
        "badge": "🌻 DEBUT ERA",
        "icon": "🦋",
        "charm": "🤠",
        "tagline": "Handwritten lyrics, porch swings, and teenage country dreams."
    },
    "fearless": {
        "bg_gradient": "linear-gradient(135deg, #fffdf0 0%, #fae8ad 100%)",
        "card_bg": "#ffffff",
        "accent": "#b8860b",
        "wristband": "#facc15",
        "text_color": "#422e03",
        "badge_bg": "#ffe082",
        "badge_text": "#5d4037",
        "shadow": "rgba(184, 134, 11, 0.22)",
        "badge": "✨ FEARLESS (TV)",
        "icon": "✨",
        "charm": "👑",
        "tagline": "Dancing in the rain with golden butterflies."
    },
    "speak now": {
        "bg_gradient": "linear-gradient(135deg, #faf3ff 0%, #ead0fc 100%)",
        "card_bg": "#ffffff",
        "accent": "#7e22ce",
        "wristband": "#c084fc",
        "text_color": "#330c4e",
        "badge_bg": "#e9d5ff",
        "badge_text": "#581c87",
        "shadow": "rgba(126, 34, 206, 0.2)",
        "badge": "💜 SPEAK NOW (TV)",
        "icon": "🐉",
        "charm": "🎆",
        "tagline": "Sparks flying, fighting dragons, and heartfelt confessions."
    },
    "red": {
        "bg_gradient": "linear-gradient(135deg, #fff3f3 0%, #ffd0d3 100%)",
        "card_bg": "#ffffff",
        "accent": "#be123c",
        "wristband": "#f43f5e",
        "text_color": "#4c0519",
        "badge_bg": "#fecdd3",
        "badge_text": "#881337",
        "shadow": "rgba(190, 18, 60, 0.22)",
        "badge": "🧣 RED (TV)",
        "icon": "🧣",
        "charm": "🍁",
        "tagline": "Passionate, burning, nostalgic, and beautifully chaotic."
    },
    "1989": {
        "bg_gradient": "linear-gradient(135deg, #f0f9ff 0%, #bee3f8 100%)",
        "card_bg": "#ffffff",
        "accent": "#0284c7",
        "wristband": "#38bdf8",
        "text_color": "#082f49",
        "badge_bg": "#bae6fd",
        "badge_text": "#0369a1",
        "shadow": "rgba(2, 132, 199, 0.2)",
        "badge": "🕶 1989 (TV)",
        "icon": "🩵",
        "charm": "🪩",
        "tagline": "Polaroids, skyline views, and unapologetic pop perfection."
    },
    "reputation": {
        "bg_gradient": "linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%)",
        "card_bg": "#ffffff",
        "accent": "#0f172a",
        "wristband": "#22c55e",
        "text_color": "#020617",
        "badge_bg": "#0f172a",
        "badge_text": "#f8fafc",
        "shadow": "rgba(15, 23, 42, 0.25)",
        "badge": "🐍 REPUTATION",
        "icon": "🐍",
        "charm": "🖤",
        "tagline": "Big reputations, dark alleys, and fiercely guarded true love."
    },
    "lover": {
        "bg_gradient": "linear-gradient(135deg, #fff0f6 0%, #fbcfe8 100%)",
        "card_bg": "#ffffff",
        "accent": "#db2777",
        "wristband": "#f472b6",
        "text_color": "#500724",
        "badge_bg": "#fce7f3",
        "badge_text": "#9d174d",
        "shadow": "rgba(219, 39, 119, 0.2)",
        "badge": "💘 LOVER",
        "icon": "💖",
        "charm": "🏹",
        "tagline": "Pastel cotton candy skies, heart sunglasses, and hopeless romance."
    },
    "folklore": {
        "bg_gradient": "linear-gradient(135deg, #fafaf9 0%, #e7e5e4 100%)",
        "card_bg": "#ffffff",
        "accent": "#57534e",
        "wristband": "#a8a29e",
        "text_color": "#1c1917",
        "badge_bg": "#e7e5e4",
        "badge_text": "#292524",
        "shadow": "rgba(87, 83, 78, 0.16)",
        "badge": "🌲 FOLKLORE",
        "icon": "🕯️",
        "charm": "🌲",
        "tagline": "Whispering pine trees, old cardigans, and untold secrets."
    },
    "evermore": {
        "bg_gradient": "linear-gradient(135deg, #fff7ed 0%, #fed7aa 100%)",
        "card_bg": "#ffffff",
        "accent": "#c2410c",
        "wristband": "#fb923c",
        "text_color": "#431407",
        "badge_bg": "#ffedd5",
        "badge_text": "#7c2d12",
        "shadow": "rgba(194, 65, 12, 0.2)",
        "badge": "🍂 EVERMORE",
        "icon": "🌲",
        "charm": "🪵",
        "tagline": "Cabin fires, willow branches, and poetic winter mysteries."
    },
    "midnights": {
        "bg_gradient": "linear-gradient(135deg, #f5f3ff 0%, #c7d2fe 100%)",
        "card_bg": "#ffffff",
        "accent": "#4338ca",
        "wristband": "#818cf8",
        "text_color": "#1e1b4b",
        "badge_bg": "#e0e7ff",
        "badge_text": "#312e81",
        "shadow": "rgba(67, 56, 202, 0.22)",
        "badge": "🌙 MIDNIGHTS",
        "icon": "🌙",
        "charm": "💎",
        "tagline": "Meet me at midnight: sleepless nights, lavender haze, and clockwork."
    },
    "the tortured poets department": {
        "bg_gradient": "linear-gradient(135deg, #fbfbfa 0%, #d6d3d1 100%)",
        "card_bg": "#ffffff",
        "accent": "#44403c",
        "wristband": "#d6d3d1",
        "text_color": "#1c1917",
        "badge_bg": "#e7e5e4",
        "badge_text": "#1c1917",
        "shadow": "rgba(68, 64, 60, 0.18)",
        "badge": "🖋 TTPD",
        "icon": "🖋️",
        "charm": "📜",
        "tagline": "Typewriters, statues, manuscript margins, and manic melancholia."
    },
    "life of a showgirl": {
        "bg_gradient": "linear-gradient(135deg, #fdf4ff 0%, #f0abfc 100%)",
        "card_bg": "#ffffff",
        "accent": "#9333ea",
        "wristband": "#e879f9",
        "text_color": "#4a044e",
        "badge_bg": "#fae8ff",
        "badge_text": "#701a75",
        "shadow": "rgba(147, 51, 234, 0.22)",
        "badge": "🎭 SHOWGIRL",
        "icon": "🎭",
        "charm": "🎟️",
        "tagline": "Glittering stage lights, heavy velvet curtains, and raw drama."
    }
}

DEFAULT_THEME = {
    "bg_gradient": "linear-gradient(135deg, #fff1f2 0%, #fecdd3 100%)",
    "card_bg": "#ffffff",
    "accent": "#e11d48",
    "wristband": "#fb7185",
    "text_color": "#3f0a1c",
    "badge_bg": "#ffe4e6",
    "badge_text": "#9f1239",
    "shadow": "rgba(225, 29, 72, 0.18)",
    "badge": "👑 THE ERAS TOUR",
    "icon": "✨",
    "charm": "⭐",
    "tagline": "The grand tournament across all eras of Taylor Swift's discography."
}

ALBUM_DATA = {
    "taylor swift": ("🌻 You're heartfelt and loyal. You believe in fairytales and handwritten notes.", "Olivia Dean",
                     "The Daydream Believer"),
    "fearless": ("✨ You're brave in love. You run toward butterflies, not away from them.", "Sabrina Carpenter",
                 "The Golden Romantic"),
    "speak now": ("💜 You're dramatic in the best way. You feel everything deeply.", "Conan Gray",
                  "The Confessional Poet"),
    "red": ("🧣 You love hard and remember everything. Passionate, nostalgic, and a little chaotic.", "Gracie Abrams",
            "The Passionate Archivist"),
    "1989": ("🕶 You're confident and independent. Reinvention looks good on you.", "Tate McRae", "The Pop Visionary"),
    "reputation": ("🐍 You're bold, magnetic, and misunderstood. You protect your heart but love fiercely.",
                   "Stray Kids", "The Untouchable Icon"),
    "lover": ("💘 You're soft but strong. Romantic, hopeful, and unapologetically emotional.", "ROSÉ",
              "The Hopeless Romantic"),
    "folklore": ("🌲 You're introspective and poetic. You find beauty in quiet moments and untold stories.", "Bon Iver",
                 "The Story Weaver"),
    "evermore": ("🍂 You're thoughtful and emotionally layered. You sit with your feelings.", "Lana Del Rey",
                 "The Autumn Philosopher"),
    "midnights": ("🌙 You're a late-night thinker. Self-aware, reflective, and a little mysterious.", "Djo",
                  "The Midnight Mastermind"),
    "the tortured poets department": ("🖋 You're intense and expressive. You turn heartbreak into art.", "Gracie Abrams",
                                      "The Tortured Wordsmith"),
    "life of a showgirl": ("🎭 You live for the spotlight but feel everything when the curtain falls.", "Chappell Roan",
                           "The Spotlight Siren")
}

EGGS = [
    "🐍 A snake slithers by... Reputation energy detected.",
    "🕯 A cardigan appears out of nowhere. Folklore found you.",
    "💄 You check the mirror. Red lipstick era activated.",
    "🌙 It's 2:13 AM. You should be sleeping. You're not.",
    "📓 You found a hidden lyric in the margins.",
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


# --- AUDIO PREVIEW VIA ITUNES SEARCH API ---
@st.cache_data(show_spinner=False)
def fetch_song_preview(song_title):
    try:
        query = urllib.parse.quote(f"Taylor Swift {song_title}")
        url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            if data['resultCount'] > 0:
                return data['results'][0].get('previewUrl')
    except Exception:
        pass
    return None


# --- INITIALIZE SESSION STATE ---
if "phase" not in st.session_state:
    st.session_state.phase = "START_HUB"
    st.session_state.game_mode = "FULL"  # "FULL", "SPEED", "TRACK5"
    st.session_state.album_ratings = {}
    st.session_state.all_song_ratings = {}
    st.session_state.album_winners = []
    st.session_state.lucky_13_count = 0
    st.session_state.current_album = None
    st.session_state.bracket_list = []
    st.session_state.bracket_winner = None
    st.session_state.bracket_step = 1
    st.session_state.final_winner = None
    st.session_state.daily_lyric = random.choice(SWIFT_LYRICS)
    st.session_state.surprise_songs = []


def get_current_theme():
    if st.session_state.current_album:
        return ERA_THEMES.get(st.session_state.current_album.lower(), DEFAULT_THEME)
    return DEFAULT_THEME


theme = get_current_theme()


# --- AUDIO AND CSS STYLING ---
def play_sound(sound_type="click"):
    freq = 520 if sound_type == "click" else 784
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


def render_friendship_bracelet(song_title, album_name=None):
    clean_title = "".join([c for c in song_title.upper() if c.isalnum() or c == " "])[:18]
    words = clean_title.split()
    era_charm = ERA_THEMES.get(album_name.lower(), DEFAULT_THEME).get("charm", "✨") if album_name else "💖"

    left_charms = ["⭐", era_charm, "💎"]
    right_charms = ["🪩", "13", "✨"]
    bead_colors = ["#fbcfe8", "#fde047", "#bae6fd", "#bbf7d0", "#ddd6fe", "#fed7aa"]

    beads_html = []
    for ch in left_charms:
        beads_html.append(f'<div class="charm-bead">{ch}</div><div class="spacer-bead"></div>')

    color_idx = 0
    for w_idx, word in enumerate(words):
        for char in word:
            c_bg = bead_colors[color_idx % len(bead_colors)]
            beads_html.append(f'<div class="bracelet-bead" style="background:{c_bg};">{char}</div>')
            color_idx += 1
        if w_idx < len(words) - 1:
            beads_html.append('<div class="heart-spacer">🤍</div>')

    for ch in right_charms:
        beads_html.append(f'<div class="spacer-bead"></div><div class="charm-bead">{ch}</div>')

    return f"""
        <div class="bracelet-container">
            <div class="bracelet-string"></div>
            <div class="beads-row">{''.join(beads_html)}</div>
        </div>
    """


st.markdown(f"""
    <style>
        .stApp {{
            background: {theme['bg_gradient']};
            color: {theme['text_color']};
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            overflow-x: hidden;
            transition: background 0.7s ease;
        }}

        /* Synced LED Stadium Wristband */
        .wristband-bar {{
            width: 100%;
            height: 12px;
            background: {theme['wristband']};
            border-radius: 6px;
            box-shadow: 0 0 20px {theme['wristband']}, 0 0 8px {theme['wristband']};
            margin-bottom: 20px;
            animation: wristbandGlow 1.8s ease-in-out infinite alternate;
        }}
        @keyframes wristbandGlow {{
            0% {{ opacity: 0.6; filter: brightness(1); }}
            100% {{ opacity: 1; filter: brightness(1.3); }}
        }}

        .era-hero {{
            position: relative;
            background: linear-gradient(135deg, #ffffff 0%, rgba(255, 255, 255, 0.88) 100%);
            border: 2px solid {theme['accent']};
            box-shadow: 0 14px 40px {theme['shadow']};
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        .hero-icon {{
            font-size: 3.5rem;
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
            background-color: {theme['card_bg']};
            border: 1.5px solid rgba(0, 0, 0, 0.06);
            box-shadow: 0 12px 30px {theme['shadow']};
            border-radius: 18px;
            padding: 22px;
            margin-bottom: 20px;
        }}

        .lyric-card {{
            background: #ffffff;
            border-left: 5px solid {theme['accent']};
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 20px;
            box-shadow: 0 4px 14px {theme['shadow']};
        }}

        /* VIP Concert Ticket & Receipt Styling */
        .vip-ticket {{
            background: #ffffff;
            border: 3px dashed {theme['accent']};
            border-radius: 20px;
            padding: 30px 24px;
            box-shadow: 0 16px 40px {theme['shadow']};
            margin-bottom: 25px;
            text-align: center;
            font-family: 'Courier New', Courier, monospace;
        }}

        /* Bracelet */
        .bracelet-container {{
            position: relative;
            padding: 28px 0;
            margin: 15px 0 25px 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .bracelet-string {{
            position: absolute;
            width: 95%;
            height: 5px;
            background: linear-gradient(90deg, #cbd5e1 0%, #94a3b8 50%, #cbd5e1 100%);
            border-radius: 3px;
            z-index: 1;
        }}
        .beads-row {{
            position: relative;
            z-index: 2;
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            max-width: 95%;
        }}
        .bracelet-bead {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 0.95rem;
            color: #18181b;
            border: 2px solid #52525b;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }}
        .charm-bead {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #ffffff;
            border: 2px solid #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.18);
        }}
        .spacer-bead {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #cbd5e1;
            margin: 0 2px;
        }}
        .heart-spacer {{
            font-size: 1.1rem;
            margin: 0 4px;
        }}

        div.stButton > button {{
            background-color: {theme['accent']};
            color: #ffffff !important;
            border: none;
            font-weight: 700;
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
    <div class="wristband-bar"></div>
""", unsafe_allow_html=True)


def trigger_random_easter_egg():
    if random.random() < 0.25:
        st.toast(random.choice(EGGS), icon="💎")


# ==============================================================================
# SCREEN 1: START HUB & GAME MODES
# ==============================================================================
if st.session_state.phase == "START_HUB":
    st.session_state.current_album = None

    st.markdown(f"""
        <div class="era-hero">
            <div class="hero-icon">✨</div>
            <div>
                <div class="era-badge">👑 WELCOME TO THE ERAS TOUR ARENA</div>
                <h1 style="margin: 0; font-size: 2.3rem; color: {theme['text_color']};">The Ultimate Taylor Swift Bracket</h1>
                <p style="margin: 4px 0 0 0; font-size: 1rem; opacity: 0.85;">Choose your tournament style below to start playing.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Lyric of the Day Marquee
    lyric_quote, lyric_source = st.session_state.daily_lyric
    st.markdown(f"""
        <div class="lyric-card">
            <div style="font-size: 1.05rem; font-style: italic; font-weight: 600; color: #334155;">{lyric_quote}</div>
            <div style="font-size: 0.82rem; color: #64748b; margin-top: 4px;">— {lyric_source}</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("### 🎮 Select Your Game Mode")

    col_mode1, col_mode2, col_mode3 = st.columns(3)

    with col_mode1:
        st.markdown("""
            <div class="era-card" style="height: 230px;">
                <h3>🎪 Full Eras Tour</h3>
                <p style="font-size: 0.9rem; color: #64748b;">Rate track-by-track through every era on a 13-point scale. Settle album ties and crown the grand champion.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Play Full Eras Tour 🎵", use_container_width=True):
            st.session_state.game_mode = "FULL"
            st.session_state.phase = "SELECT_ALBUM"
            st.rerun()

    with col_mode2:
        st.markdown("""
            <div class="era-card" style="height: 230px;">
                <h3>⚡ Speed Run Bracket</h3>
                <p style="font-size: 0.9rem; color: #64748b;">Skip all sliders! 16 randomly seeded iconic Taylor Swift anthems go straight into sudden-death voting.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Play Speed Run ⚡", use_container_width=True):
            st.session_state.game_mode = "SPEED"
            contenders = list(SPEED_RUN_POOL)
            random.shuffle(contenders)
            st.session_state.bracket_list = contenders
            st.session_state.bracket_winner = contenders[0]
            st.session_state.bracket_step = 1
            st.session_state.phase = "FINAL_BRACKET"
            st.rerun()

    with col_mode3:
        st.markdown("""
            <div class="era-card" style="height: 230px;">
                <h3>💔 Track 5 Gauntlet</h3>
                <p style="font-size: 0.9rem; color: #64748b;">The ultimate emotional showdown. Only Taylor's legendary Track 5s battle for the #1 crown.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Play Track 5 Gauntlet 💔", use_container_width=True):
            st.session_state.game_mode = "TRACK5"
            t5_contenders = [song for song, _ in TRACK_5_SONGS]
            random.shuffle(t5_contenders)
            st.session_state.bracket_list = t5_contenders
            st.session_state.bracket_winner = t5_contenders[0]
            st.session_state.bracket_step = 1
            st.session_state.phase = "FINAL_BRACKET"
            st.rerun()

# ==============================================================================
# SCREEN 2: ALBUM HUB (FULL MODE)
# ==============================================================================
elif st.session_state.phase == "SELECT_ALBUM":
    st.session_state.current_album = None

    st.markdown(f"""
        <div class="era-hero">
            <div class="hero-icon">👑</div>
            <div>
                <div class="era-badge">ERA SELECTION HUB</div>
                <h1 style="margin: 0; font-size: 2.2rem; color: {theme['text_color']};">The Eras Tour Arena</h1>
                <p style="margin: 4px 0 0 0; font-size: 1rem; opacity: 0.85;">Choose an album below to rate on the 13-point scale.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    completed_ratio = len(st.session_state.album_ratings) / len(all_albums)
    st.progress(completed_ratio,
                text=f"Tour Progress: {len(st.session_state.album_ratings)} of {len(all_albums)} Eras Ranked")

    grid_cols = st.columns(3)
    for idx, alb in enumerate(all_albums):
        c = grid_cols[idx % 3]
        meta = ERA_THEMES.get(alb.lower(), DEFAULT_THEME)
        is_done = alb in st.session_state.album_ratings

        with c:
            st.markdown(f"""
                <div style="background:{meta['card_bg']}; border-radius:14px; border:2px solid {meta['accent'] if not is_done else '#94a3b8'}; padding:16px; margin-bottom:12px; box-shadow: 0 4px 12px {meta['shadow']};">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-size: 2rem;">{meta['icon']}</span>
                        <span style="font-size: 1.4rem;">{meta['charm']}</span>
                    </div>
                    <div style="font-weight: 800; font-size: 1.1rem; color:{meta['text_color']}; margin: 6px 0 2px 0;">{alb}</div>
                    <div style="font-size: 0.83rem; color:{meta['text_color']}; opacity: 0.85;">
                        {'✅ Completed (' + str(round(st.session_state.album_ratings[alb], 2)) + '/13)' if is_done else meta['tagline']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if not is_done:
                if st.button(f"Enter {alb}", key=f"btn_alb_{idx}", use_container_width=True):
                    play_sound("click")
                    trigger_random_easter_egg()
                    st.session_state.current_album = alb
                    st.session_state.phase = "RATE_ALBUM"
                    st.rerun()

    if st.session_state.album_winners:
        st.divider()
        if st.button("🏆 Start The Ultimate Showdown Early", use_container_width=True):
            play_sound("fanfare")
            st.session_state.bracket_list = list(st.session_state.album_winners)
            random.shuffle(st.session_state.bracket_list)
            st.session_state.bracket_winner = st.session_state.bracket_list[0]
            st.session_state.bracket_step = 1
            st.session_state.phase = "FINAL_BRACKET"
            st.rerun()

# ==============================================================================
# SCREEN 3: RATE SONGS IN CURRENT ERA
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
# SCREEN 4: HEAD-TO-HEAD BRACKET & AUDIO PREVIEWS
# ==============================================================================
elif st.session_state.phase in ["ALBUM_TIEBREAKER", "FINAL_BRACKET"]:
    is_final = (st.session_state.phase == "FINAL_BRACKET")
    contenders = st.session_state.bracket_list
    current_champ = st.session_state.bracket_winner
    step = st.session_state.bracket_step

    badge_text = "🏆 GRAND FINALE SHOWDOWN" if is_final else f"⚡ {st.session_state.current_album.upper()} TIEBREAKER"

    st.markdown(f"""
        <div class="era-hero">
            <div class="hero-icon">⚔️</div>
            <div>
                <div class="era-badge">{badge_text}</div>
                <h1 style="margin: 0; font-size: 2.2rem; color: {theme['text_color']};">Head-to-Head Arena</h1>
                <p style="margin: 4px 0 0 0; font-size: 1rem; opacity: 0.85;">Listen to preview clips and vote for the track that advances.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if step < len(contenders):
        challenger = contenders[step]
        progress_val = step / (len(contenders) - 1)
        st.progress(progress_val, text=f"Showdown {step} of {len(contenders) - 1}")

        st.markdown('<div class="era-card">', unsafe_allow_html=True)
        c1, c_vs, c2 = st.columns([5, 1, 5])

        with c1:
            st.markdown(f"#### 👑 Defending Track\n### {current_champ}")
            champ_audio = fetch_song_preview(current_champ)
            if champ_audio:
                st.audio(champ_audio)
            if st.button(f"Vote '{current_champ}'", key=f"champ_{step}", use_container_width=True):
                play_sound("click")
                trigger_random_easter_egg()
                st.session_state.bracket_step += 1
                st.rerun()

        with c_vs:
            st.markdown(f"""
                <div style="text-align: center; margin-top: 50px;">
                    <span style="background: {theme['accent']}; color: #fff; padding: 6px 12px; border-radius: 999px; font-weight: 800; font-size: 0.9rem;">
                        VS
                    </span>
                </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"#### ⚡ Challenger\n### {challenger}")
            chal_audio = fetch_song_preview(challenger)
            if chal_audio:
                st.audio(chal_audio)
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
            # Pick 2 random surprise songs
            all_songs = songs_df["Song"].tolist()
            st.session_state.surprise_songs = random.sample([s for s in all_songs if s != winner], 2)
            st.session_state.phase = "RESULTS"
            st.rerun()

# ==============================================================================
# SCREEN 5: RESULTS, VIP PASS, RECEIPT & SURPRISE SONGS
# ==============================================================================
elif st.session_state.phase == "RESULTS":
    st.balloons()
    play_sound("fanfare")

    # Determine Era context
    if st.session_state.game_mode == "FULL" and st.session_state.album_ratings:
        best_album = max(st.session_state.album_ratings, key=st.session_state.album_ratings.get)
        best_score = st.session_state.album_ratings[best_album]
    else:
        best_album = "The Eras Tour"
        best_score = 13.0

    best_meta = ERA_THEMES.get(best_album.lower(), DEFAULT_THEME)

    st.markdown(f"""
        <div class="era-hero">
            <div class="hero-icon">{best_meta['icon']}</div>
            <div>
                <div class="era-badge">✨ OFFICIAL TOURNAMENT RESULTS</div>
                <h1 style="margin: 0; font-size: 2.2rem; color: {theme['text_color']};">Champion Song: {st.session_state.final_winner}</h1>
                <p style="margin: 4px 0 0 0; font-size: 1rem; opacity: 0.85;">{best_meta['tagline']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Friendship Bracelet
    st.write("### 📿 Your Custom Friendship Bracelet")
    st.markdown(render_friendship_bracelet(st.session_state.final_winner, best_album), unsafe_allow_html=True)

    # Surprise Songs of the Night Wheel
    st.markdown(f"""
        <div class="era-card" style="border-left: 6px solid {theme['accent']};">
            <h3 style="margin-top:0;">🎹 Tonight's Acoustic Surprise Songs</h3>
            <p style="margin-bottom: 5px;">Acoustic Guitar: <strong>✨ {st.session_state.surprise_songs[0]}</strong></p>
            <p style="margin-bottom: 0;">Piano: <strong>✨ {st.session_state.surprise_songs[1]}</strong></p>
        </div>
    """, unsafe_allow_html=True)

    # VIP Concert Ticket & Eras Receipt
    meta_personality = ALBUM_DATA.get(best_album.lower(), (
        "You have elite taste across every single era.",
        "Taylor Swift",
        "The Pop Visionary"
    ))

    st.markdown(f"""
        <div class="vip-ticket">
            <div style="font-size: 1.2rem; font-weight: bold; letter-spacing: 2px;">*** THE ERAS TOUR VIP PASS ***</div>
            <div style="font-size: 0.85rem; color: #71717a;">DATE: 13 DECEMBER | SECTION: 13 | ROW: 13 | SEAT: 13</div>
            <hr style="border: 1px dashed #d4d4d8; margin: 15px 0;">
            <div style="font-size: 1.4rem; font-weight: 800; color: {best_meta['accent']};">{st.session_state.final_winner.upper()}</div>
            <div style="font-size: 0.95rem; margin-top: 5px;">OFFICIAL #1 ERA CHAMPION</div>
            <hr style="border: 1px dashed #d4d4d8; margin: 15px 0;">
            <div style="text-align: left; max-width: 380px; margin: 0 auto; font-size: 0.88rem; line-height: 1.6;">
                ERA SOULMATE : {best_album.upper()}<br>
                SWIFTIE TITLE: {meta_personality[2]}<br>
                MATCHED ARTIST: {meta_personality[1]}<br>
                TOTAL 13s LOGGED: {st.session_state.lucky_13_count}
            </div>
            <div style="margin-top: 20px; font-size: 1.8rem; letter-spacing: 6px;">||| | |||| || | ||| |||| |</div>
            <div style="font-size: 0.75rem; color: #a1a1aa;">THANK YOU FOR ATTENDING THE ERAS TOUR</div>
        </div>
    """, unsafe_allow_html=True)

    # Mastermind Mode Check
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

    # Export Button & Reset
    if st.session_state.all_song_ratings:
        sorted_songs = sorted(st.session_state.all_song_ratings.items(), key=lambda x: x[1], reverse=True)[:50]
        export_df = pd.DataFrame(sorted_songs, columns=["Song", "Rating"])
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