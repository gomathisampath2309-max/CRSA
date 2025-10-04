import gspread
from google.colab import auth
from google.auth import default
import ipywidgets as widgets
from IPython.display import display, clear_output

# 🔹 Authenticate with Google
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# 🔹 Open Google Sheet (must already exist in your Drive)
SPREADSHEET_NAME = "Study_Master"   # Change if your sheet has a different name
spreadsheet = gc.open(SPREADSHEET_NAME)
sheet = spreadsheet.sheet1

# 🔹 Create form widgets
StudyID = widgets.Text(description="StudyID")
StudyName = widgets.Text(description="StudyName")
Indication = widgets.Text(description="Indication")
LineOfTherapy = widgets.Text(description="Therapy")
Mutation = widgets.Text(description="Mutation")
TotalSlots = widgets.IntText(description="Slots")
Status = widgets.Dropdown(description="Status", options=["Active", "Closed", "Planned"])
StartDate = widgets.Text(description="StartDate", placeholder="dd-mm-yyyy")
EndDate = widgets.Text(description="EndDate", placeholder="dd-mm-yyyy")

submit_btn = widgets.Button(description="Submit ✅", button_style='success')
output = widgets.Output()

# 🔹 Submit function
def on_submit(b):
    with output:
        clear_output()
        new_row = [
            StudyID.value,
            StudyName.value,
            Indication.value,
            LineOfTherapy.value,
            Mutation.value,
            str(TotalSlots.value),
            Status.value,
            StartDate.value,
            EndDate.value,
        ]
        sheet.append_row(new_row)
        print(f"✅ Study {StudyID.value} added successfully to Google Sheets!")

submit_btn.on_click(on_submit)

# 🔹 Display form
display(StudyID, StudyName, Indication, LineOfTherapy, Mutation, 
        TotalSlots, Status, StartDate, EndDate, submit_btn, output)
