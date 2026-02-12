import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="PE Show Notes 2026",
    page_icon="\U0001f3ad",
    layout="wide",
)

DATA_FILE = "show_notes_data.json"

SHOW_ORDER = [
    (1, "Footloose", "Large Tap Group"), (2, "Poison", "Daytona Hip Hop"), (3, "Dark Outside", "Isabella Acro"), (4, "Glow In The Dark", "Ellie Lyrical"), (5, "The Water Lillies", "Clara Hadley Naomi Ballet"), (6, "Mambo Italiano", "Skittles Jazz"), (7, "The Phoenix", "Kristyn Pointe"), (8, "When Falling Stars Fly", "Addison Contemp"), (9, "Crushin", "Chelsea Jazz"), (10, "Still Rock Roll To Me", "Elite Contemp"), (11, "Watch This", "Kristyn Daytona Jazz"), (12, "If I Had My Way", "Kaylee Acro"), (13, "Love Is A Compass", "Abby Lyrical"), (14, "First Flight", "Sharpie Acro"), (15, "Clair De Lune", "Clara Ballet"), (16, "Yo Te Extranare", "Isabella Kristyn Kaylee Acro"), (17, "Get Ready", "Adult Jazz"), (18, "My Strongest Suit", "Nevaeh Jazz"), (19, "I Wanna Be A Rockette", "Rosie Jazz"), (20, "Undertow", "Livewire Contemp"), (21, "A Wizards Plan", "Nevaeh Chelsea Open"), (22, "Two Sides Of The Same Coin", "Ryleigh Abby Hip Hop"), (23, "Another Day Of Sun", "Jordyn Ella Audry Jazz"), (24, "Fast", "Mikaela Jazz"), (25, "Time Of Your Life", "Elite Tap"), (26, "Bad Thoughts", "Larissa Lyrical"), (27, "You Make My Dreams Come True", "Chelsea Tap"), (28, "Divertissement", "Ella Jordyn Nevaeh Ballet"), (29, "Predator", "Elite Jazz"), (30, "Fly On", "Abby Naomi Ryleigh Tap"), (31, "Show Out", "Marley Hip Hop"), (32, "Creep", "Clara Open"), (33, "Two Player Game", "Daytona Kristyn Theatre"), (34, "The Lab", "Sharpie Hip Hop"), (35, "Mind Reader", "Olivia Jazz"), (36, "Snowing", "Hadley Lyrical"), (37, "Cant Smile Without You", "Ella Contemp"), (38, "Red Riding Hood", "Madelyn Ballet"), (39, "Hope", "LW Acro"), (40, "Blackbird", "Naomi Tap"), (41, "Hide And Seek", "Sharpie Contemp"), (42, "Not Gonna Take It", "Adult Theatre"), (43, "The Tea Party", "Rosie Ballet"), (44, "Race You", "Ella Tap"), (45, "Respect", "LWPH Jazz"), (0, "--- BREAK ---", ""), (46, "Connection", "SHLW Open"), (48, "Dance", "Nevaeh Addison Jazz"), (49, "Sun", "Olivia Contemp"), (50, "Home", "Elite Acro"), (51, "Pose", "Jordyn Ella Hip Hop"), (52, "Hit The Road Jack", "Hadley Jazz"), (53, "Still", "PH Lyrical"), (54, "Young And Beautiful", "Kristyn Acro"), (55, "Suspicious Minds", "Kaylee Contemp"), (56, "Under Pressure", "Abby Sydney Tap"), (57, "Waltz Of The Flowers", "Sharpie Ballet"), (58, "Fever", "Clara Jazz"), (59, "May Breezes", "Naomi Ballet"), (60, "Hunter", "Kristyn Contemp"), (61, "Soda Pop", "Chelsea Ellie Jazz"), (62, "It Never Ends", "Jordyn Lyrical"), (63, "Ive Come To Realize", "LW Lyrical"), (64, "I Love Play Rehearsal", "Kailyn Theatre"), (65, "Swagger Jagger", "Callie Jazz"), (66, "Always", "Nevaeh Lyrical"), (67, "Tyler", "PH Hip Hop"), (68, "Monster", "Daytona Kristyn Kaylee Hip Hop"), (69, "Because We Believe", "Isabella Clara Lyrical"), (70, "Wind It Up", "Sharpie Jazz"), (71, "You Will Be Found", "Sydney Olivia Lyrical"), (72, "Dangerous", "Kristyn Jazz"), (73, "Dollar", "PH Contemp"), (74, "Dance Of The Garden", "Jordyn Ballet"), (75, "Shawty Get Loose", "Amiya Hip Hop"), (76, "Friend Like Me", "Addison Tap"), (77, "Born To Do", "LW PH Theatre"), (78, "Le Tango Noir", "Mikaela Open"), (79, "You Will Be Found", "Sydney Tap"), (80, "Life Of The Party", "Ellie Acro"), (81, "Throwback Love", "Nevaeh Tap"), (82, "Recess Riot", "Skittles Hip Hop"), (83, "A Dream", "Kristyn Lyrical"), (84, "Lost At Sea", "Clara Contemp"), (85, "Death Wish", "Isabella Lyrical"), (86, "Girls", "Sharpie Lyrical"), (87, "You Dont Know Me", "Ryleigh Hip Hop"), (88, "Nuvole Bianche", "LWPH Ballet"), (89, "Yellow", "Daytona Lyrical"), (90, "Say You Love Me", "Madison Lyrical"), (91, "Be Aggressive", "Sharpie Theatre"), (92, "Landslide", "Abby Tap"), (93, "We The North", "LW Hip Hop"),
]


def load_notes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_notes(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_all_staff_names(notes_data):
    staff_names = set()
    for routine_notes in notes_data.values():
        for note in routine_notes:
            staff_names.add(note['staff'])
    return sorted(list(staff_names))


def main():
    st.markdown(
        """<h1 style='text-align:center;'>\U0001f3ad Pure Energy Dance Studio</h1>
        <h3 style='text-align:center;'>Comp Show 2026 - Staff Notes</h3><hr>""",
        unsafe_allow_html=True,
    )

    notes_data = load_notes()

    tab_enter, tab_review = st.tabs(["\U0001f4dd Enter Notes", "\U0001f4cb Review All Notes"])

    with tab_enter:
        col_left, col_right = st.columns([1, 2])

        with col_left:
            st.subheader("Select Routine")
            routine_options = []
            for num, title, dancers in SHOW_ORDER:
                if num == 0:
                    routine_options.append("--- BREAK ---")
                else:
                    routine_options.append(f"#{num} - {title} ({dancers})")

            selected = st.selectbox(
                "Choose a routine:",
                routine_options,
                index=0,
                label_visibility="collapsed",
            )

            staff_name = st.text_input("Your Name:", placeholder="Enter your name")

        with col_right:
            if selected != "--- BREAK ---":
                st.subheader(f"Notes for: {selected}")

                key = selected.split(" - ")[0].strip()

                existing = notes_data.get(key, [])
                if existing:
                    st.markdown("**Previous Notes:**")
                    for note in existing:
                        st.info(
                            f"**{note['staff']}** ({note['time']}):\n\n{note['note']}"
                        )

                note_text = st.text_area(
                    "Add your note:",
                    height=150,
                    placeholder="Type your notes about this routine here...",
                    key=f"note_{key}",
                )

                col_a, col_b = st.columns([1, 3])
                with col_a:
                    if st.button("\U0001f4be Save Note", type="primary", use_container_width=True):
                        if not staff_name.strip():
                            st.error("Please enter your name.")
                        elif not note_text.strip():
                            st.error("Please enter a note.")
                        else:
                            if key not in notes_data:
                                notes_data[key] = []
                            notes_data[key].append(
                                {
                                    "staff": staff_name.strip(),
                                    "note": note_text.strip(),
                                    "time": datetime.now().strftime(
                                        "%b %d, %Y %I:%M %p"
                                    ),
                                }
                            )
                            save_notes(notes_data)
                            st.success("Note saved!")
                            st.rerun()
            else:
                st.subheader("\U00002615 Intermission Break")
                st.write("No notes needed for the break.")

    with tab_review:
        st.subheader("All Saved Notes")

        notes_data = load_notes()

        if not notes_data:
            st.info("No notes have been saved yet.")
        else:
            all_staff = get_all_staff_names(notes_data)
                        
            # Backup/Export button
            import csv
            import io
            
            # Create CSV export
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer)
            csv_writer.writerow(["Routine", "Notes"]
            
            for num, title, dancers in SHOW_ORDER:
                if num == 0:
                    continue
                key = f"#{num}"
                if key in notes_data:
                    for note in notes_data[key]:
                    csv_writer.writerow([f"{title} - {dancers}", note['note']])            
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="\U0001f4be Download All Notes (CSV)",
                data=csv_data,
                file_name=f"show_notes_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Download all notes as a CSV file for backup"
            )
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                staff_filter_options = ["All Staff"] + all_staff
                selected_staff = st.selectbox(
                    "\U0001f464 Filter by Staff:",
                    staff_filter_options,
                    index=0,
                )
            
            with col2:
                search = st.text_input(
                    "\U0001f50d Search notes:",
                    placeholder="Search by routine, dancer, or note content..."
                )

            for num, title, dancers in SHOW_ORDER:
                if num == 0:
                    st.markdown("---")
                    st.markdown("### \U00002615 BREAK")
                    st.markdown("---")
                    continue
                    
                key = f"#{num}"
                if key in notes_data and notes_data[key]:
                    filtered_notes = notes_data[key]
                    if selected_staff != "All Staff":
                        filtered_notes = [n for n in filtered_notes if n['staff'] == selected_staff]
                    
                    if not filtered_notes:
                        continue
                    
                    display_label = f"#{num} - {title} ({dancers})"
                    
                    if search:
                        search_lower = search.lower()
                        match = search_lower in display_label.lower()
                        if not match:
                            for n in filtered_notes:
                                if search_lower in n['staff'].lower() or search_lower in n['note'].lower():
                                    match = True
                                    break
                        if not match:
                            continue

                    with st.expander(f"\U0001f3b5 {display_label} ({len(filtered_notes)} note{'s' if len(filtered_notes) != 1 else ''})"):
                        for note in filtered_notes:
                            st.markdown(
                                f"**{note['staff']}** - *{note['time']}*"
                            )
                            st.write(note["note"])
                            st.markdown("---")

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:gray;'>Pure Energy Dance Studio - Comp Show 2026</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
