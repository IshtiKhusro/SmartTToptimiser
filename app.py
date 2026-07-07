from flask import Flask, render_template, request
import random

app = Flask(__name__)

# -----------------------------
# Teacher Availability
# -----------------------------
teacher_availability = {
    "Rahul Sir": ["Monday", "Wednesday", "Friday"],
    "Anita Maam": ["Tuesday", "Thursday"]
}

# -----------------------------
# Subject -> Teacher Mapping
# -----------------------------
subject_teacher = {
    "Math": "Rahul Sir",
    "Physics": "Rahul Sir",
    "Chemistry": "Anita Maam",
    "English": "Anita Maam",
    "Biology": "Rahul Sir",
    "Programming": "Rahul Sir",
    "History": "Anita Maam",
    "Economics": "Anita Maam",
    "AI": "Rahul Sir",
    "DBMS": "Rahul Sir"
}

# -----------------------------
# Subject Priority
# -----------------------------
priority = {
    "Math": 5,
    "Physics": 5,
    "Programming": 5,
    "AI": 5,
    "DBMS": 4,
    "Chemistry": 4,
    "Biology": 3,
    "English": 2,
    "History": 1,
    "Economics": 1
}

# -----------------------------
# Available Rooms
# -----------------------------
rooms = [
    "Room 101",
    "Room 102",
    "Room 103",
    "Lab 1",
    "Lab 2"
]

# -----------------------------
# Working Days
# -----------------------------
days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

# -----------------------------
# Time Slots
# -----------------------------
slots = [
    "09:00 - 10:00",
    "10:00 - 11:00",
    "11:00 - 12:00",
    "01:00 - 02:00",
    "02:00 - 03:00",
    "03:00 - 04:00"
]
# -----------------------------
# Generate Smart Timetable
# -----------------------------
def generate_timetable(subjects):

    # Schedule high-priority subjects first
    subjects.sort(
        key=lambda x: priority.get(x["subject"], 1),
        reverse=True
    )

    timetable = []

    teacher_schedule = {}
    room_schedule = {}

    slot_index = 0

    for subject in subjects:

        subject_name = subject["subject"]
        hours = int(subject["hours"])

        teacher = subject_teacher.get(subject_name, "Not Assigned")

        classes_assigned = 0

        # Allocate required number of hours
        while classes_assigned < hours:

            assigned = False

            for day in teacher_availability.get(teacher, days):

                current_slot = slots[slot_index]

                teacher_key = (teacher, day, current_slot)

                room = random.choice(rooms)

                room_key = (room, day, current_slot)

                # Conflict checking
                if teacher_key not in teacher_schedule and room_key not in room_schedule:

                    teacher_schedule[teacher_key] = True
                    room_schedule[room_key] = True

                    timetable.append({
                        "day": day,
                        "slot": current_slot,
                        "subject": subject_name,
                        "teacher": teacher,
                        "room": room,
                        "hours": 1
                    })

                    classes_assigned += 1

                    slot_index += 1

                    if slot_index >= len(slots):
                        slot_index = 0

                    assigned = True
                    break

            # If no slot found
            if not assigned:

                timetable.append({
                    "day": "Not Available",
                    "slot": "-",
                    "subject": subject_name,
                    "teacher": teacher,
                    "room": "-",
                    "hours": 1
                })

                classes_assigned += 1

    # Sort timetable by day then slot
    day_order = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Not Available": 5
    }

    timetable.sort(
        key=lambda x: (
            day_order.get(x["day"], 6),
            x["slot"]
        )
    )

    return timetable
# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Generate Timetable
# -----------------------------
@app.route("/generate", methods=["GET", "POST"])
def generate():

    if request.method == "POST":

        subjects = []

        # Read unlimited subjects from the form
        i = 1

        while True:

            subject = request.form.get(f"subject{i}")
            hours = request.form.get(f"hours{i}")

            # Stop when no more subject fields exist
            if subject is None:
                break

            if subject.strip() != "":

                subjects.append({
                    "subject": subject,
                    "hours": hours
                })

            i += 1

        timetable = generate_timetable(subjects)

        # Dashboard statistics
        stats = {
            "total_classes": len(timetable),
            "total_subjects": len(subjects),
            "teachers": len(set(item["teacher"] for item in timetable)),
            "rooms": len(set(item["room"] for item in timetable if item["room"] != "-"))
        }

        return render_template(
            "result.html",
            timetable=timetable,
            stats=stats
        )

    return render_template("generate.html")


# -----------------------------
# About Page
# -----------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# -----------------------------
# Contact Page
# -----------------------------
@app.route("/contact")
def contact():
    return render_template("contact.html")


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)