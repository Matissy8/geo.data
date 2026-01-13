import customtkinter as ctk
from tkintermapview import TkinterMapView
from tkinter import messagebox
import math

# ---------------- CONFIG ----------------
TRIGGER_DISTANCE_METERS = 30

CENTER_LAT = 56.96135571506875
CENTER_LON = 23.735643336261624
LOCK_ZOOM = 19

points = [
    {"lat": 56.961420, "lon": 23.735610, "question": "Jautājums 1", "answered": False},
    {"lat": 56.961300, "lon": 23.735700, "question": "Jautājums 2", "answered": False},
    {"lat": 56.961360, "lon": 23.735520, "question": "Jautājums 3", "answered": False},
]

# ---------------- UTILS ----------------
def distance_m(lat1, lon1, lat2, lon2):
    dx = (lon2 - lon1) * 111320 * math.cos(math.radians(lat1))
    dy = (lat2 - lat1) * 111320
    return math.sqrt(dx*dx + dy*dy)

# ---------------- SIDEBAR ----------------
class QuestionSidebar(ctk.CTkFrame):
    def __init__(self, master, questions):
        super().__init__(master, width=260, corner_radius=0)
        self.pack_propagate(False)

        self.questions = questions
        self.labels = []

        title = ctk.CTkLabel(self, text="Jautājumi", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=15)

        for i, q in enumerate(self.questions):
            lbl = ctk.CTkLabel(
                self,
                text=f"{i+1}. {q['question']}",
                wraplength=220,
                justify="left",
                anchor="w"
            )
            lbl.pack(fill="x", padx=15, pady=8)
            self.labels.append(lbl)

    def mark_answered(self, index):
        self.labels[index].configure(text_color="gray")

# ---------------- APP ----------------
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("1000x600")
app.title("Orientēšanās – Pumpuru vidusskola")

# Sidebar
sidebar = QuestionSidebar(app, points)
sidebar.pack(side="left", fill="y")

# Map
map_widget = TkinterMapView(app, corner_radius=0)
map_widget.pack(side="right", fill="both", expand=True)
map_widget.set_position(CENTER_LAT, CENTER_LON)
map_widget.set_zoom(LOCK_ZOOM)
map_widget.set_tile_server(
    "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=20
)

# Mark points
for p in points:
    map_widget.set_marker(p["lat"], p["lon"], text="Punkts")

# Disable map movement
map_widget.canvas.bind("<B1-Motion>", lambda e: "break")
map_widget.canvas.bind("<ButtonPress-1>", lambda e: "break")
map_widget.canvas.bind("<MouseWheel>", lambda e: "break")
map_widget.canvas.bind("<Button-4>", lambda e: "break")
map_widget.canvas.bind("<Button-5>", lambda e: "break")

# Player marker
user_marker = None

def check_points(user_lat, user_lon):
    for i, p in enumerate(points):
        if not p["answered"]:
            if distance_m(user_lat, user_lon, p["lat"], p["lon"]) <= TRIGGER_DISTANCE_METERS:
                p["answered"] = True
                sidebar.mark_answered(i)

def on_map_click(coords):
    global user_marker
    lat, lon = coords

    # Keep map centered
    map_widget.set_position(CENTER_LAT, CENTER_LON)

    if user_marker:
        user_marker.delete()
    user_marker = map_widget.set_marker(lat, lon, text="Tu")

    check_points(lat, lon)

map_widget.add_left_click_map_command(on_map_click)

app.mainloop()

