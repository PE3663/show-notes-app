import streamlit as st
import json
import os
import csv
import io
from datetime import datetime
from streamlit_mic_recorder import speech_to_text

st.set_page_config(
    page_title="PE Show Notes",
    page_icon="\U0001f3ad",
    layout="centered",
)

DATA_DIR = "show_data"
SHOWS_FILE = "shows_config.json"

COMP_2026_ROUTINES = [
    (1, "Footloose", "Large Tap Group"), (2, "Poison", "Daytona Hip Hop"), (3, "Dark Outside", "Isabella Acro"), (4, "Glow In The Dark", "Ellie Lyrical"),
    (5, "The Water Lillies", "Clara Hadley Naomi Ballet"), (6, "Mambo Italiano", "Skittles Jazz"), (7, "The Phoenix", "Kristyn Pointe"), (8, "When Falling Stars Fly", "Addison Contemp"),
    (9, "Crushin", "Chelsea Jazz"), (10, "Still Rock Roll To Me", "Elite Contemp"), (11, "Watch This", "Kristyn Daytona Jazz"), (12, "If I Had My Way", "Kaylee Acro"),
    (13, "Love Is A Compass", "Abby Lyrical"), (14, "First Flight", "Sharpie Acro"), (15, "Clair De Lune", "Clara Ballet"), (16, "Yo Te Extranare", "Isabella Kristyn Kaylee Acro"),
    (17, "Get Ready", "Adult Jazz"), (18, "My Strongest Suit", "Nevaeh Jazz"), (19, "I Wanna Be A Rockette", "Rosie Jazz"), (20, "Undertow", "Livewire Contemp"),
    (21, "A Wizards Plan", "Nevaeh Chelsea Open"), (22, "Two Sides Of The Same Coin", "Ryleigh Abby Hip Hop"), (23, "Another Day Of Sun", "Jordyn Ella Audry Jazz"), (24, "Fast", "Mikaela Jazz"),
    (25, "Time Of Your Life", "Elite Tap"), (26, "Bad Thoughts", "Larissa Lyrical"), (27, "You Make My Dreams Come True", "Chelsea Tap"), (28, "Divertissement", "Ella Jordyn Nevaeh Ballet"),
    (29, "Predator", "Elite Jazz"), (30, "Fly On", "Abby Naomi Ryleigh Tap"), (31, "Show Out", "Marley Hip Hop"), (32, "Creep", "Clara Open"),
    (33, "Two Player Game", "Daytona Kristyn Theatre"), (34, "The Lab", "Sharpie Hip Hop"), (35, "Mind Reader", "Olivia Jazz"), (36, "Snowing", "Hadley Lyrical"),
    (37, "Cant Smile Without You", "Ella Contemp"), (38, "Red Riding Hood", "Madelyn Ballet"), (39, "Hope", "LW Acro"), (40, "Blackbird", "Naomi Tap"),
    (41, "Hide And Seek", "Sharpie Contemp"), (42, "Not Gonna Take It", "Adult Theatre"), (43, "The Tea Party", "Rosie Ballet"), (44, "Race You", "Ella Tap"),
    (45, "Respect", "LWPH Jazz"), (0, "--- BREAK ---", ""), (46, "Connection", "SHLW Open"), (48, "Dance", "Nevaeh Addison Jazz"),
    (49, "Sun", "Olivia Contemp"), (50, "Home", "Elite Acro"), (51, "Pose", "Jordyn Ella Hip Hop"), (52, "Hit The Road Jack", "Hadley Jazz"),
    (53, "Still", "PH Lyrical"), (54, "Young And Beautiful", "Kristyn Acro"), (55, "Suspicious Minds", "Kaylee Contemp"), (56, "Under Pressure", "Abby Sydney Tap"),
    (57, "Waltz Of The Flowers", "Sharpie Ballet"), (58, "Fever", "Clara Jazz"), (59, "May Breezes", "Naomi Ballet"), (60, "Hunter", "Kristyn Contemp"),
    (61, "Soda Pop", "Chelsea Ellie Jazz"), (62, "It Never Ends", "Jordyn Lyrical"), (63, "Ive Come To Realize", "LW Lyrical"), (64, "I Love Play Rehearsal", "Kailyn Theatre"),
    (65, "Swagger Jagger", "Callie Jazz"), (66, "Always", "Nevaeh Lyrical"), (67, "Tyler", "PH Hip Hop"), (68, "Monster", "Daytona Kristyn Kaylee Hip Hop"),
    (69, "Because We Believe", "Isabella Clara Lyrical"), (70, "Wind It Up", "Sharpie Jazz"), (71, "You Will Be Found", "Sydney Olivia Lyrical"), (72, "Dangerous", "Kristyn Jazz"),
    (73, "Dollar", "PH Contemp"), (74, "Dance Of The Garden", "Jordyn Ballet"), (75, "Shawty Get Loose", "Amiya Hip Hop"), (76, "Friend Like Me", "Addison Tap"),
    (77, "Born To Do", "LW PH Theatre"), (78, "Le Tango Noir", "Mikaela Open"), (79, "You Will Be Found", "Sydney Tap"), (80, "Life Of The Party", "Ellie Acro"),
    (81, "Throwback Love", "Nevaeh Tap"), (82, "Recess Riot", "Skittles Hip Hop"), (83, "A Dream", "Kristyn Lyrical"), (84, "Lost At Sea", "Clara Contemp"),
    (85, "Death Wish", "Isabella Lyrical"), (86, "Girls", "Sharpie Lyrical"), (87, "You Dont Know Me", "Ryleigh Hip Hop"), (88, "Nuvole Bianche", "LWPH Ballet"),
    (89, "Yellow", "Daytona Lyrical"), (90, "Say You Love Me", "Madison Lyrical"), (91, "Be Aggressive", "Sharpie Theatre"), (92, "Landslide", "Abby Tap"),
    (93, "We The North", "LW Hip Hop"),
]

def load_shows():
    if os.path.exists(SHOWS_FILE):
        with open(SHOWS_FILE, "r") as f:
            return json.load(f)
    default = {"Comp Show 2026": {"routines": "COMP_2026", "created": "Feb 12, 2026"}}
    save_shows(default)
    return default

def save_shows(data):
    with open(SHOWS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_notes_file(show_name):
    safe = show_name.replace(" ", "_").replace("/", "_").lower()
    return f"notes_{safe}.json"

def load_notes(show_name):
    fn = get_notes_file(show_name)
    if os.path.exists(fn):
        with open(fn, "r") as f:
            return json.load(f)
    old = "show_notes_data.json"
    if show_name == "Comp Show 2026" and os.path.exists(old):
        with open(old, "r") as f:
            return json.load(f)
    return {}

def save_notes(show_name, data):
    with open(get_notes_file(show_name), "w") as f:
        json.dump(data, f, indent=2)

def delete_note(show_name, routine_key, note_index):
    nd = load_notes(show_name)
    if routine_key in nd and 0 <= note_index < len(nd[routine_key]):
        del nd[routine_key][note_index]
        if not nd[routine_key]:
            del nd[routine_key]
        save_notes(show_name, nd)
        return True
    return False

def get_all_staff_names(notes_data):
    names = set()
    for rn in notes_data.values():
        for n in rn:
            names.add(n['staff'])
    return sorted(list(names))

def get_routines(show_name, shows):
    info = shows.get(show_name, {})
    rt = info.get("routines", "")
    if rt == "COMP_2026":
        return COMP_2026_ROUTINES
    custom = info.get("custom_routines", [])
    return [(r[0], r[1], r[2]) for r in custom]

def parse_routines_text(text):
    routines = []
    lines = text.strip().split("\n")
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        if line.upper() == "BREAK" or line == "---":
            routines.append((0, "--- BREAK ---", ""))
            continue
        if "|" in line:
            parts = line.split("|")
            title = parts[0].strip()
            dancers = parts[1].strip() if len(parts) > 1 else ""
        elif "-" in line:
            parts = line.split("-", 1)
            title = parts[0].strip()
            dancers = parts[1].strip() if len(parts) > 1 else ""
        else:
            title = line
            dancers = ""
        routines.append((i, title, dancers))
    return routines

def main():
    shows = load_shows()
    st.markdown(
        """
# \U0001f3ad Pure Energy Dance Studio
### Staff Notes
---
""",
        unsafe_allow_html=True,
    )
    show_names = list(shows.keys())
    if not show_names:
        show_names = ["Comp Show 2026"]
    selected_show = st.selectbox("\U0001f3ac Select Show:", show_names, index=0)
    show_order = get_routines(selected_show, shows)
    notes_data = load_notes(selected_show)
    tab_enter, tab_review, tab_manage = st.tabs(["\U0001f4dd Enter Notes", "\U0001f4cb Review All Notes", "\U00002699\ufe0f Manage Shows"])
    with tab_enter:
        if not show_order:
            st.warning("This show has no routines yet. Go to Manage Shows to add routines.")
        else:
            st.subheader("Select Routine")
            routine_options = []
            for num, title, dancers in show_order:
                if num == 0:
                    routine_options.append("--- BREAK ---")
                else:
                    routine_options.append(f"#{num} - {title} ({dancers})")
            selected = st.selectbox("Choose a routine:", routine_options, index=0, label_visibility="collapsed")
            staff_name = st.text_input("Your Name:", placeholder="Enter your name")
            if selected != "--- BREAK ---":
                st.subheader(f"Notes for: {selected}")
                key = selected.split(" - ")[0].strip()
                existing = notes_data.get(key, [])
                if existing:
                    st.markdown("**Previous Notes:**")
                    for note in existing:
                        st.info(f"**{note['staff']}** ({note['time']}):\\n\\n{note['note']}")

                            # Voice-to-text input
            st.markdown("**🎤 Voice Input:** Click to record, click again to stop")
            voice_text = speech_to_text(language='en', use_container_width=True, just_once=True, key=f'voice_{key}')

                            # Initialize or update note content with voice input
            if f'note_content_{key}' not in st.session_state:
                st.session_state[f'note_content_{key}'] = ''
                            if voice_text:
                                                if st.session_state[f'note_content_{key}']:
                                                                        st.session_state[f'note_content_{key}'] += ' ' + voice_text
                                                                    else:
                                                                                            st.session_state[f'note_content_{key}'] = voice_text

