import customtkinter as ctk
import json
import qrcode
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import random
import string

# Set up theme and appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class TicketBookingApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("FastTicket")

        self.root.geometry("1000x800")  # Increased window size

        # Email configuration
        self.email_config = {
            "sender_email": "dhruv_22134501021@hnbgu.edu.in",
            "sender_password": "app_password",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587
        }

        # Color scheme
        self.colors = {
            "primary": "#f0f0f0",
            "secondary": "#ffffff",
            "accent": "#808080",
            "text": "#2d2d2d",
            "booked": "#ff4444"  # Red color for booked seats
        }

        # File paths
        self.booking_data_file = "bookings.json"
        self.theater_data_file = "data.json"
        self.qr_code_dir = "qrcodes"

        # Initialize data
        self.bookings = self.load_bookings()
        self.current_booking = {}
        self.selected_seats = []
        self.seat_buttons = []

        # Create necessary directories
        self.initialize_directories()

        # Build UI
        self.create_main_frame()
        self.show_theater_selection()

        self.root.mainloop()

    def get_booked_seats(self):
        """Get all booked seats for current theater and movie"""
        booked_seats = []
        for booking in self.bookings.values():
            if (booking["theater"] == self.current_booking.get("theater") and
                    (booking["movie"] == self.current_booking.get("movie")) and
                    booking["valid"]):
                booked_seats.extend(booking["seats"])
        return booked_seats

    def initialize_directories(self):
        if not os.path.exists(self.qr_code_dir):
            os.makedirs(self.qr_code_dir)

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors["primary"])
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def load_bookings(self):
        try:
            if os.path.exists(self.booking_data_file):
                with open(self.booking_data_file, "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading bookings: {e}")
        return {}

    def save_booking(self):
        try:
            self.bookings[self.current_booking["id"]] = self.current_booking
            with open(self.booking_data_file, "w") as f:
                json.dump(self.bookings, f, indent=4)
        except Exception as e:
            print(f"Error saving booking: {e}")

    def show_theater_selection(self):
        self.clear_frame()

        try:
            with open(self.theater_data_file, "r") as f:
                theaters_data = json.load(f)

            ctk.CTkLabel(self.main_frame, text="Select Theater",
                         font=("Arial", 20, "bold"), text_color=self.colors["text"]).pack(pady=15)

            for theater in theaters_data["theatres"]:
                btn = ctk.CTkButton(self.main_frame, text=theater,
                                    command=lambda t=theater: self.show_movie_selection(t),
                                    fg_color=self.colors["accent"], hover_color="#666666",
                                    font=("Arial", 14), height=35)
                btn.pack(pady=8, fill="x", padx=40)
        except Exception as e:
            ctk.CTkLabel(self.main_frame, text="Error loading theaters",
                         text_color="red").pack(pady=20)
            print(f"Error loading theaters: {e}")

    def show_movie_selection(self, theater):
        self.current_booking["theater"] = theater
        self.clear_frame()

        try:
            with open(self.theater_data_file, "r") as f:
                movies = json.load(f)["theatres"][theater]

            ctk.CTkLabel(self.main_frame, text="Select Movie",
                         font=("Arial", 20, "bold"), text_color=self.colors["text"]).pack(pady=15)

            for movie in movies:
                btn = ctk.CTkButton(self.main_frame, text=movie,
                                    command=lambda m=movie: self.show_seat_selection(m),
                                    fg_color=self.colors["accent"], hover_color="#666666",
                                    font=("Arial", 14), height=35)
                btn.pack(pady=8, fill="x", padx=40)
        except Exception as e:
            ctk.CTkLabel(self.main_frame, text="Error loading movies",
                         text_color="red").pack(pady=20)
            print(f"Error loading movies: {e}")

    def show_seat_selection(self, movie):
        self.current_booking["movie"] = movie
        self.clear_frame()

        seat_layout = ctk.CTkFrame(self.main_frame, fg_color=self.colors["secondary"], corner_radius=15)
        seat_layout.pack(pady=10, fill="both", expand=True)

        # Add screen display
        ctk.CTkLabel(seat_layout, text="~ SCREEN ~",
                     font=("Arial", 16, "bold"), text_color=self.colors["text"]
                     ).pack(pady=(15, 10))

        seats_frame = ctk.CTkFrame(seat_layout, fg_color=self.colors["secondary"])
        seats_frame.pack(pady=10)

        self.selected_seats = []
        self.seat_buttons = []
        booked_seats = self.get_booked_seats()

        # Generate 2 rows of 10 seats each
        for row in range(2):
            row_frame = ctk.CTkFrame(seats_frame, fg_color=self.colors["secondary"])
            row_frame.pack(pady=2)
            for col in range(10):
                seat_num = row * 10 + col + 1
                is_booked = seat_num in booked_seats

                btn = ctk.CTkButton(row_frame, text=str(seat_num), width=35, height=35,
                                    fg_color=self.colors["booked"] if is_booked else "#e0e0e0",
                                    hover_color="#c0c0c0",
                                    text_color=self.colors["text"],
                                    command=lambda sn=seat_num: self.toggle_seat(sn) if not is_booked else None)
                btn.configure(state="disabled" if is_booked else "normal")
                btn.pack(side="left", padx=2, pady=2)
                self.seat_buttons.append(btn)

        ctk.CTkButton(seat_layout, text="Continue", command=self.show_personal_details,
                      fg_color=self.colors["accent"], hover_color="#666666",
                      font=("Arial", 14), width=120).pack(pady=15)

    def toggle_seat(self, seat_num):
        if seat_num in self.selected_seats:
            self.selected_seats.remove(seat_num)
            self.seat_buttons[seat_num - 1].configure(fg_color="#e0e0e0")
        else:
            self.selected_seats.append(seat_num)
            self.seat_buttons[seat_num - 1].configure(fg_color=self.colors["accent"])

    def show_personal_details(self):
        if not self.selected_seats:
            return

        self.current_booking["seats"] = sorted(self.selected_seats)
        self.clear_frame()

        form_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["secondary"], corner_radius=15)
        form_frame.pack(pady=10, fill="both", expand=True)

        ctk.CTkLabel(form_frame, text="Personal Details",
                     font=("Arial", 18, "bold"), text_color=self.colors["text"]).pack(pady=15)

        entries = []
        fields = ["Full Name:", "Email:"]
        for field in fields:
            frame = ctk.CTkFrame(form_frame, fg_color=self.colors["secondary"])
            frame.pack(fill="x", padx=30, pady=8)

            label = ctk.CTkLabel(frame, text=field, font=("Arial", 14),
                                 text_color=self.colors["text"], width=100)
            label.pack(side="left")

            entry = ctk.CTkEntry(frame, font=("Arial", 14), width=200,
                                 fg_color=self.colors["primary"], border_color="#cccccc")
            entry.pack(side="right")
            entries.append(entry)

        self.name_entry, self.email_entry = entries

        ctk.CTkButton(form_frame, text="Confirm Booking", command=self.confirm_booking,
                      fg_color=self.colors["accent"], hover_color="#666666",
                      font=("Arial", 14), width=120).pack(pady=20)

    def generate_qr(self, data):
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="red", back_color="white")
            filename = f"{self.qr_code_dir}/{self.current_booking['id']}.png"
            img.save(filename)
            return filename
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None

    def send_email_with_qr(self):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.email_config["sender_email"]
            msg["To"] = self.current_booking["email"]
            msg["Subject"] = "Your Movie Ticket - FastTicket"

            text = f"""
            Thank you for booking with FastTicket, {self.current_booking['name']}!

            Here are your ticket details:

            Name: {self.current_booking['name']}
            Movie: {self.current_booking['movie']}
            Theater: {self.current_booking['theater']}
            Seats: {', '.join(map(str, self.current_booking['seats']))}
            Total: ₹{len(self.current_booking['seats']) * 200}

            Please find your QR code attached. Present this at the theater entrance.
            """
            msg.attach(MIMEText(text))

            qr_path = self.generate_qr(self.current_booking["id"])
            if qr_path:
                with open(qr_path, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-Disposition", "attachment", filename="ticket_qr.png")
                    msg.attach(img)

            server = smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"])
            server.starttls()
            server.login(self.email_config["sender_email"], self.email_config["sender_password"])
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def show_confirmation_screen(self):
        self.clear_frame()
        success_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["secondary"], corner_radius=15)
        success_frame.pack(pady=20, fill="both", expand=True)

        ctk.CTkLabel(success_frame, text="Booking Confirmed!",
                     font=("Arial", 24, "bold"), text_color="green").pack(pady=20)

        ctk.CTkLabel(success_frame, text="Check your email for tickets and QR code",
                     font=("Arial", 16)).pack(pady=10)

        btn_frame = ctk.CTkFrame(success_frame)
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Book Again", command=self.restart_booking,
                      fg_color=self.colors["accent"], hover_color="#666666",
                      font=("Arial", 14)).pack(side="left", padx=20)

        ctk.CTkButton(btn_frame, text="Exit", command=self.root.destroy,
                      fg_color="#ff4444", hover_color="#cc0000",
                      font=("Arial", 14)).pack(side="left", padx=20)

    def restart_booking(self):
        self.current_booking = {}
        self.selected_seats = []
        self.bookings = self.load_bookings()
        self.show_theater_selection()

    def confirm_booking(self):
        if not all([self.name_entry.get(), self.email_entry.get()]):
            ctk.CTkLabel(self.main_frame, text="Please fill all fields!",
                         text_color="red").pack(pady=5)
            return

        self.current_booking.update({
            "id": ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            "name": self.name_entry.get(),
            "email": self.email_entry.get(),
            "valid": True
        })

        self.save_booking()

        if self.send_email_with_qr():
            self.show_confirmation_screen()
        else:
            ctk.CTkLabel(self.main_frame, text="Booking failed. Please try again.",
                         font=("Arial", 14), text_color=self.colors["accent"]).pack(pady=15)


if __name__ == "__main__":
    TicketBookingApp()