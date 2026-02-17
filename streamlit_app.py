import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import csv
import io
from datetime import datetime

st.set_page_config(
    page_title="PE Show Notes 2026",
    page_icon="\U0001f3ad",
    layout="centered",
)


# --- Google Sheets Connection ----
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

@st.cache_resource
def get_gsheet_connection():
    """Create a connection to Google Sheets using service account credentials."""
    creds_dict = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def get_worksheet():
    """Get the show notes worksheet, create if it doesn't exist."""
    client = get_gsheet_connection()
    spreadsheet_id = st.secrets["SPREADSHEET_ID"]
    sh = client.open_by_key(spreadsheet_id)
    try:
        ws = sh.worksheet("ShowNotes")
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title="ShowNotes", rows=1000, cols=4)
        ws.append_row(["routine_key", "staff", "note", "time"])
    return ws

def load_notes():
    """Load all notes from Google Sheets into a dict."""
    try:
        ws = get_worksheet()
        records = ws.get_all_records()
        notes_data = {}
        for row in records:
            key = row["routine_key"]
            if key not in notes_data:
                notes_data[key] = []
            notes_data[key].append({
                "staff": row["staff"],
                "note": row["note"],
                "time": row["time"],
            })
        return notes_data
    except Exception as e:
        st.error(f"Error loading notes: {e}")
        return {}

def save_note(routine_key, staff, note_text):
    """Save a new note to Google Sheets."""
    try:
        ws = get_worksheet()
        timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p")
        ws.append_row([routine_key, staff, note_text, timestamp])
        return True
    except Exception as e:
        st.error(f"Error saving note: {e}")
        return False

def delete_note(routine_key, staff, time_str):
    """Delete a note from Google Sheets by matching key, staff, and time."""
    try:
        ws = get_worksheet()
        records = ws.get_all_values()
        for i, row in enumerate(records):
            if i == 0:
                continue  # skip header
            if row[0] == routine_key and row[1] == staff and row[3] == time_str:
                ws.delete_rows(i + 1)
                return True
        return False
    except Exception as e:
        st.error(f"Error deleting note: {e}")
        return False

def check_admin_password(password):
    """Check if the entered password matches the admin password."""
    try:
        return password == st.secrets["ADMIN_PASSWORD"]
    except (KeyError, FileNotFoundError):
        return False

def get_all_staff_names(notes_data):
    staff_names = set()
    for routine_notes in notes_data.values():
        for note in routine_notes:
            staff_names.add(note['staff'])
    return sorted(list(staff_names))

SHOW_ORDER = [
    (1, "Footloose", "Large Tap Group"),
    (2, "Poison", "Daytona Hip Hop"),
    (3, "Dark Outside", "Isabella Acro"),
    (4, "Glow In The Dark", "Ellie Lyrical"),
    (5, "The Water Lillies", "Clara Hadley Naomi Ballet"),
    (6, "Mambo Italiano", "Skittles Jazz"),
    (7, "The Phoenix", "Kristyn Pointe"),
    (8, "When Falling Stars Fly", "Addison Contemp"),
    (9, "Crushin", "Chelsea Jazz"),
    (10, "Still Rock Roll To Me", "Elite Contemp"),
    (11, "Watch This", "Kristyn Daytona Jazz"),
    (12, "If I Had My Way", "Kaylee Acro"),
    (13, "Love Is A Compass", "Abby Lyrical"),
    (14, "First Flight", "Sharpie Acro"),
    (15, "Clair De Lune", "Clara Ballet"),
    (16, "Yo Te Extranare", "Isabella Kristyn Kaylee Acro"),
    (17, "Get Ready", "Adult Jazz"),
    (18, "My Strongest Suit", "Nevaeh Jazz"),
    (19, "I Wanna Be A Rockette", "Rosie Jazz"),
    (20, "Undertow", "Livewire Contemp"),
    (21, "A Wizards Plan", "Nevaeh Chelsea Open"),
    (22, "Two Sides Of The Same Coin", "Ryleigh Abby Hip Hop"),
    (23, "Another Day Of Sun", "Jordyn Ella Audry Jazz"),
    (24, "Fast", "Mikaela Jazz"),
    (25, "Time Of Your Life", "Elite Tap"),
    (26, "Bad Thoughts", "Larissa Lyrical"),
    (27, "You Make My Dreams Come True", "Chelsea Tap"),
    (28, "Divertissement", "Ella Jordyn Nevaeh Ballet"),
    (29, "Predator", "Elite Jazz"),
    (30, "Fly On", "Abby Naomi Ryleigh Tap"),
    (31, "Show Out", "Marley Hip Hop"),
    (32, "Creep", "Clara Open"),
    (33, "Two Player Game", "Daytona Kristyn Theatre"),
    (34, "The Lab", "Sharpie Hip Hop"),
    (35, "Mind Reader", "Olivia Jazz"),
    (36, "Snowing", "Hadley Lyrical"),
    (37, "Cant Smile Without You", "Ella Contemp"),
    (38, "Red Riding Hood", "Madelyn Ballet"),
    (39, "Hope", "LW Acro"),
    (40, "Blackbird", "Naomi Tap"),
    (41, "Hide And Seek", "Sharpie Contemp"),
    (42, "Not Gonna Take It", "Adult Theatre"),
    (43, "The Tea Party", "Rosie Ballet"),
    (44, "Race You", "Ella Tap"),
    (45, "Respect", "LWPH Jazz"),
    (0, "--- BREAK ---", ""),
    (46, "Connection", "SHLW Open"),
    (48, "Dance", "Nevaeh Addison Jazz"),
    (49, "Sun", "Olivia Contemp"),
    (50, "Home", "Elite Acro"),
    (51, "Pose", "Jordyn Ella Hip Hop"),
    (52, "Hit The Road Jack", "Hadley Jazz"),
    (53, "Still", "PH Lyrical"),
    (54, "Young And Beautiful", "Kristyn Acro"),
    (55, "Suspicious Minds", "Kaylee Contemp"),
    (56, "Under Pressure", "Abby Sydney Tap"),
    (57, "Waltz Of The Flowers", "Sharpie Ballet"),
    (58, "Fever", "Clara Jazz"),
    (59, "May Breezes", "Naomi Ballet"),
    (60, "Hunter", "Kristyn Contemp"),
    (61, "Soda Pop", "Chelsea Ellie Jazz"),
    (62, "It Never Ends", "Jordyn Lyrical"),
    (63, "Ives Come To Realize", "LW Lyrical"),
    (64, "I Love Play Rehearsal", "Kailyn Theatre"),
    (65, "Swagger Jagger", "Callie Jazz"),
    (66, "Always", "Nevaeh Lyrical"),
    (67, "Tyler", "PH Hip Hop"),
    (68, "Monster", "Daytona Kristyn Kaylee Hip Hop"),
    (69, "Because We Believe", "Isabella Clara Lyrical"),
    (70, "Wind It Up", "Sharpie Jazz"),
    (71, "You Will Be Found", "Sydney Olivia Lyrical"),
    (72, "Dangerous", "Kristyn Jazz"),
    (73, "Dollar", "PH Contemp"),
    (74, "Dance Of The Garden", "Jordyn Ballet"),
    (75, "Shawty Get Loose", "Amiya Hip Hop"),
    (76, "Friend Like Me", "Addison Tap"),
    (77, "Born To Do", "LW PH Theatre"),
    (78, "Le Tango Noir", "Mikaela Open"),
    (79, "You Will Be Found", "Sydney Tap"),
    (80, "Life Of The Party", "Ellie Acro"),
    (81, "Throwback Love", "Nevaeh Tap"),
    (82, "Recess Riot", "Skittles Hip Hop"),
    (83, "A Dream", "Kristyn Lyrical"),
    (84, "Lost At Sea", "Clara Contemp"),
    (85, "Death Wish", "Isabella Lyrical"),
    (86, "Girls", "Sharpie Lyrical"),
    (87, "You Dont Know Me", "Ryleigh Hip Hop"),
    (88, "Nuvole Bianche", "LWPH Ballet"),
    (89, "Yellow", "Daytona Lyrical"),
    (90, "Say You Love Me", "Madison Lyrical"),
    (91, "Be Aggressive", "Sharpie Theatre"),
    (92, "Landslide", "Abby Tap"),
    (93, "We The North", "LW Hip Hop"),
]

def main():
    st.markdown(
        """
        # \U0001f3ad Pure Energy Dance Studio
        ### Comp Show 2026 - Staff Notes
        ---
        """,
        unsafe_allow_html=True,
    )

    staff_name = st.text_input("Your Name:", placeholder="Enter your name")

    tab_enter, tab_review = st.tabs(["\U0001f4dd Enter Notes", "\U0001f512 Review All Notes"])

    with tab_enter:
        st.subheader("Select Routine")

        routine_options = []
        for num, title, dancers in SHOW_ORDER:
            if num == 0:
                routine_options.append("--- BREAK ---")
            else:
                routine_options.append(f"#{num} - {title} ({dancers})")

        # --- Track routine index in session_state ---
        if "routine_index" not in st.session_state:
            st.session_state.routine_index = 0

        selected = st.selectbox(
            "Choose a routine:",
            routine_options,
            index=st.session_state.routine_index,
            label_visibility="collapsed",
        )

        # Keep index synced if staff manually picks from dropdown
        st.session_state.routine_index = routine_options.index(selected)

        # --- Progress indicator ---
        st.caption(f"Routine {st.session_state.routine_index + 1} of {len(routine_options)}")

        if selected != "--- BREAK ---":
            st.subheader(f"Notes for: {selected}")
            key = selected.split(" - ")[0].strip()
            notes_data = load_notes()
            existing = notes_data.get(key, [])
            if existing:
                st.markdown("**Previous Notes:**")
                for note in existing:
                    st.info(
                        f"**{note['staff']}** ({note['time']}): \n\n{note['note']}"
                    )

            note_text = st.text_area(
                "Add your note:",
                height=150,
                placeholder="Type your notes about this routine here...",
                key=f"note_{key}",
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                prev_disabled = st.session_state.routine_index == 0
                if st.button("Previous", use_container_width=True, disabled=prev_disabled):
                    st.session_state.routine_index -= 1
                    st.rerun()

            with col2:
                if st.button(
                    "Save Note",
                    type="primary",
                    use_container_width=True,
                ):
                    if not staff_name.strip():
                        st.error("Please enter your name.")
                    elif not note_text.strip():
                        st.error("Please enter a note.")
                    else:
                        if save_note(key, staff_name.strip(), note_text.strip()):
                            st.success("Note saved!")
                            st.rerun()

            with col3:
                next_disabled = st.session_state.routine_index >= len(routine_options) - 1
                if st.button("Next", use_container_width=True, disabled=next_disabled):
                    st.session_state.routine_index += 1
                    st.rerun()

        else:
            st.subheader("\u2615 Intermission Break")
            st.write("No notes needed for the break.")

            # Still show Previous/Next on break so they can navigate past it
            col1, col2, col3 = st.columns(3)

            with col1:
                prev_disabled = st.session_state.routine_index == 0
                if st.button("Previous", use_container_width=True, disabled=prev_disabled, key="break_prev"):
                    st.session_state.routine_index -= 1
                    st.rerun()

            with col3:
                next_disabled = st.session_state.routine_index >= len(routine_options) - 1
                if st.button("Next", use_container_width=True, disabled=next_disabled, key="break_next"):
                    st.session_state.routine_index += 1
                    st.rerun()

    with tab_review:
        st.subheader("Review All Notes")
        admin_password = st.text_input(
            "\U0001f512 Enter Password:",
            type="password",
            placeholder="Enter password to access notes",
            key="admin_pw",
        )
        is_admin = check_admin_password(admin_password)
        if not admin_password:
            st.info("\U0001f512 This section is password protected. Enter the password above to view all staff notes.")
        elif not is_admin:
            st.error("\u274c Incorrect password. Please try again.")
        else:
            st.success("\U0001f513 Access granted - viewing all staff notes")
            notes_data = load_notes()
            if not notes_data:
                st.info("No notes have been saved yet.")
            else:
                all_staff = get_all_staff_names(notes_data)
                # Create CSV export
                csv_buffer = io.StringIO()
                csv_writer = csv.writer(csv_buffer)
                csv_writer.writerow(["Routine", "Staff", "Note", "Time"])
                for num, title, dancers in SHOW_ORDER:
                    if num == 0:
                        continue
                    key = f"#{num}"
                    if key in notes_data and notes_data[key]:
                        for note in notes_data[key]:
                            csv_writer.writerow([f"{title} - {dancers}", note['staff'], note['note'], note['time']])
                csv_data = csv_buffer.getvalue()
                st.download_button(
                    label="\U0001f4be Download All Notes (CSV)",
                    data=csv_data,
                    file_name=f"show_notes_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    help="Download all notes as a CSV file for backup",
                )
                st.markdown("---")
                # Staff filter
                staff_filter_options = ["All Staff"] + all_staff
                selected_staff = st.selectbox(
                    "\U0001f464 Filter by Staff:",
                    staff_filter_options,
                    index=0,
                )
                search = st.text_input(
                    "\U0001f50d Search notes:",
                    placeholder="Search by routine, dancer, or note content...",
                )
                for num, title, dancers in SHOW_ORDER:
                    if num == 0:
                        st.markdown("---")
                        st.markdown("### \u2615 BREAK")
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
                        with st.expander(
                            f"\U0001f3b5 {display_label} ({len(filtered_notes)} note{'s' if len(filtered_notes) != 1 else ''})"
                        ):
                            for idx, note in enumerate(filtered_notes):
                                st.markdown(
                                    f"**{note['staff']}** - *{note['time']}*"
                                )
                                st.write(note["note"])
                                # Delete button
                                delete_key = f"delete_{key}_{note['staff']}_{note['time']}_{idx}"
                                if st.button("\U0001f5d1\ufe0f Delete Note", key=delete_key):
                                    if delete_note(key, note['staff'], note['time']):
                                        st.success("Note deleted successfully!")
                                        st.rerun()
                                st.markdown("---")

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>Pure Energy Dance Studio - Comp Show 2026</div>",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
