import cv2
from pyzbar import pyzbar
import customtkinter as ctk
import json
import os
from PIL import Image, ImageTk

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class WebcamQRValidator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FastTicket Live Validator")
        self.geometry("1200x800")

        self.bookings_file = "bookings.json"
        self.cap = None
        self.scanning = False
        self.current_ticket = None

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Webcam frame
        self.webcam_frame = ctk.CTkFrame(self)
        self.webcam_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        self.webcam_label = ctk.CTkLabel(self.webcam_frame, text="")
        self.webcam_label.pack(pady=10)

        # Control buttons
        btn_frame = ctk.CTkFrame(self.webcam_frame)
        btn_frame.pack(pady=10)

        self.toggle_btn = ctk.CTkButton(btn_frame, text="Start Scanning",
                                        command=self.toggle_scanning)
        self.toggle_btn.pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="Exit", command=self.on_close,
                      fg_color="#ff4444", hover_color="#cc0000").pack(side="left", padx=10)

        # Details frame
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        # Create labels for ticket details
        self.detail_labels = {}
        fields = [
            ("status", "Status:"),
            ("ticket_id", "Ticket ID:"),
            ("name", "Name:"),
            ("email", "Email:"),
            ("theater", "Theater:"),
            ("movie", "Movie:"),
            ("seats", "Seats:"),
            ("total", "Total:")
        ]

        for idx, (key, label) in enumerate(fields):
            self.detail_labels[key] = {
                "label": ctk.CTkLabel(self.details_frame, text=label, font=("Arial", 14, "bold")),
                "value": ctk.CTkLabel(self.details_frame, text="", font=("Arial", 14))
            }
            self.detail_labels[key]["label"].grid(row=idx, column=0, padx=10, pady=5, sticky="e")
            self.detail_labels[key]["value"].grid(row=idx, column=1, padx=10, pady=5, sticky="w")

        self.status_label = ctk.CTkLabel(self.details_frame, text="Scan a ticket...",
                                         font=("Arial", 16, "bold"))
        self.status_label.grid(row=len(fields) + 1, columnspan=2, pady=20)

        self.invalidate_btn = ctk.CTkButton(self.details_frame, text="Mark as Used",
                                            command=self.mark_as_used,
                                            fg_color="#ff4444", hover_color="#cc0000")
        self.invalidate_btn.grid(row=len(fields) + 2, columnspan=2, pady=10)

    def toggle_scanning(self):
        self.scanning = not self.scanning
        if self.scanning:
            self.start_scanning()
            self.toggle_btn.configure(text="Stop Scanning")
        else:
            self.stop_scanning()
            self.toggle_btn.configure(text="Start Scanning")
        self.clear_details()

    def start_scanning(self):
        self.cap = cv2.VideoCapture(0)
        self.scanning = True
        self.update_webcam()

    def stop_scanning(self):
        self.scanning = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.webcam_label.configure(image=None)

    def update_webcam(self):
        if self.scanning and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.process_frame(frame)
            self.after(10, self.update_webcam)

    def process_frame(self, frame):
        decoded = pyzbar.decode(frame)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if decoded:
            qr_data = decoded[0].data.decode()
            self.handle_ticket(qr_data)
            cv2.rectangle(img, (decoded[0].rect.left, decoded[0].rect.top),
                          (decoded[0].rect.left + decoded[0].rect.width,
                           decoded[0].rect.top + decoded[0].rect.height),
                          (0, 255, 0), 2)

        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(image=img)
        self.webcam_label.configure(image=img_tk)
        self.webcam_label.image = img_tk

    def handle_ticket(self, ticket_id):
        try:
            with open(self.bookings_file, "r") as f:
                bookings = json.load(f)

            if ticket_id not in bookings:
                self.clear_details()
                self.status_label.configure(text="INVALID TICKET", text_color="red")
                return

            self.current_ticket = bookings[ticket_id]
            self.current_ticket["id"] = ticket_id
            self.update_details()

        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")

    def update_details(self):
        status_color = "green" if self.current_ticket["valid"] else "orange"
        status_text = "VALID" if self.current_ticket["valid"] else "USED"

        self.detail_labels["status"]["value"].configure(
            text=status_text,
            text_color=status_color
        )
        self.detail_labels["ticket_id"]["value"].configure(
            text=self.current_ticket["id"]
        )
        self.detail_labels["name"]["value"].configure(
            text=self.current_ticket["name"]
        )
        self.detail_labels["email"]["value"].configure(
            text=self.current_ticket["email"]
        )
        self.detail_labels["theater"]["value"].configure(
            text=self.current_ticket["theater"]
        )
        self.detail_labels["movie"]["value"].configure(
            text=self.current_ticket["movie"]
        )
        self.detail_labels["seats"]["value"].configure(
            text=", ".join(map(str, self.current_ticket["seats"]))
        )
        self.detail_labels["total"]["value"].configure(
            text=f"₹{len(self.current_ticket['seats']) * 200}"
        )

        if self.current_ticket["valid"]:
            self.status_label.configure(text="VALID TICKET - SCAN SUCCESSFUL", text_color="green")
            self.invalidate_btn.configure(state="normal")
        else:
            self.status_label.configure(text="TICKET ALREADY USED", text_color="orange")
            self.invalidate_btn.configure(state="disabled")

    def clear_details(self):
        for key in self.detail_labels:
            self.detail_labels[key]["value"].configure(text="")
        self.status_label.configure(text="Scan a ticket...", text_color="black")
        self.invalidate_btn.configure(state="disabled")

    def mark_as_used(self):
        if self.current_ticket and self.current_ticket["valid"]:
            try:
                with open(self.bookings_file, "r") as f:
                    bookings = json.load(f)

                bookings[self.current_ticket["id"]]["valid"] = False

                with open(self.bookings_file, "w") as f:
                    json.dump(bookings, f, indent=4)

                self.current_ticket["valid"] = False
                self.update_details()

            except Exception as e:
                self.status_label.configure(text=f"Error: {str(e)}", text_color="red")

    def on_close(self):
        self.stop_scanning()
        self.destroy()


if __name__ == "__main__":
    validator = WebcamQRValidator()
    validator.mainloop()