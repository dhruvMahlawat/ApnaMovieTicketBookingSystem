import customtkinter as ctk
import json
import os
from tkinter import messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class AdminSystem:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("FastTicket")
        self.root.geometry("1400x900")
        self.root.configure(fg_color="#1a1a1a")

        # Custom color scheme
        self.colors = {
            "primary": "#1a1a1a",
            "secondary": "#2a2a2a",
            "accent": "#ff6b6b",
            "danger": "#d32f2f",
            "success": "#00c853",
            "text": "#ffffff"
        }

        self.data_file = "data.json"
        self.theatre_data = self.load_data()

        self.show_login_screen()
        self.root.mainloop()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                return json.load(f)
        return {"theatres": {}}

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.theatre_data, f, indent=4)

    def show_login_screen(self):
        self.login_frame = ctk.CTkFrame(self.root, fg_color=self.colors["secondary"], corner_radius=25)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Login header
        ctk.CTkLabel(self.login_frame, text="Admin Login",
                     font=("Arial", 28, "bold"), text_color=self.colors["accent"]).pack(pady=40, padx=60)

        # Modern input fields
        input_style = {
            "font": ("Arial", 18),
            "width": 400,
            "height": 60,
            "border_width": 2,
            "corner_radius": 10,
            "border_color": "#4a4a4a"
        }

        self.username = ctk.CTkEntry(self.login_frame, placeholder_text="👤 Admin ", **input_style)
        self.username.pack(pady=15)

        self.password = ctk.CTkEntry(self.login_frame, placeholder_text="🔑 Password", show="*", **input_style)
        self.password.pack(pady=15)

        # Login button
        ctk.CTkButton(self.login_frame, text="ACCESS DASHBOARD", command=self.check_login,
                      font=("Arial", 18, "bold"), width=300, height=60, corner_radius=15,
                      fg_color=self.colors["accent"], hover_color="#ff5252").pack(pady=30)

    def check_login(self):
        if self.username.get() == "admin" and self.password.get() == "admin":
            self.login_frame.destroy()
            self.show_admin_panel()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def show_admin_panel(self):
        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(pady=40, padx=40, fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", pady=20)
        ctk.CTkLabel(header, text="Movie Management Dashboard",
                     font=("Arial", 24, "bold"), text_color=self.colors["accent"]).pack()

        # Control buttons
        control_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        control_frame.pack(fill="x", pady=30)

        button_style = {
            "width": 220,
            "height": 70,
            "corner_radius": 15,
            "font": ("Arial", 16, "bold"),
            "border_width": 2,
            "border_color": self.colors["accent"]
        }

        ctk.CTkButton(control_frame, text="ADD THEATRE", command=self.add_theatre_popup,
                      **button_style, fg_color="transparent", hover_color="#1ea62e").pack(side="left", padx=15)
        ctk.CTkButton(control_frame, text="ADD MOVIE", command=self.add_movie_popup,
                      **button_style, fg_color="transparent", hover_color="#1ea62e").pack(side="left", padx=15)
        ctk.CTkButton(control_frame, text="DELETE THEATRE", command=self.delete_theatre_popup,
                      **button_style, fg_color="transparent", hover_color="#b71c1c").pack(side="left", padx=15)
        ctk.CTkButton(control_frame, text="DELETE MOVIE", command=self.delete_movie_popup,
                      **button_style, fg_color="transparent", hover_color="#b71c1c").pack(side="left", padx=15)

        # Content area
        self.scroll_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)

        self.refresh_theatre_display()

    def refresh_theatre_display(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for theatre, movies in self.theatre_data["theatres"].items():
            # Theatre card
            tile = ctk.CTkFrame(self.scroll_frame, corner_radius=20, fg_color=self.colors["secondary"])
            tile.pack(pady=15, fill="x", padx=10)

            # Theatre header
            header_frame = ctk.CTkFrame(tile, fg_color="transparent")
            header_frame.pack(fill="x", padx=20, pady=15)
            ctk.CTkLabel(header_frame, text=f"🏛️ {theatre}",
                         font=("Arial", 20, "bold"), text_color=self.colors["accent"]).pack(side="left")

            # Movies list
            movies_frame = ctk.CTkFrame(tile, fg_color="transparent")
            movies_frame.pack(fill="x", padx=30, pady=(0, 15))

            for movie in movies:
                ctk.CTkLabel(movies_frame, text=f"🎬 {movie}",
                             font=("Arial", 16), text_color=self.colors["text"]).pack(side="left", padx=15, pady=5)

    def create_popup(self, title, size):
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry(size)
        popup.grab_set()
        popup.configure(fg_color=self.colors["primary"])
        popup.resizable(False, False)
        return popup

    def add_theatre_popup(self):
        popup = self.create_popup("ADD THEATRE", "600x400")

        ctk.CTkLabel(popup, text="ENTER THEATRE NAME:", font=("Arial", 20),
                     text_color=self.colors["accent"]).pack(pady=30)

        self.theatre_entry = ctk.CTkEntry(popup, placeholder_text="Theatre Name...",
                                          font=("Arial", 18), width=400, height=60,
                                          border_width=2, corner_radius=10)
        self.theatre_entry.pack()

        ctk.CTkButton(popup, text="CREATE THEATRE", command=lambda: self.save_theatre(popup),
                      font=("Arial", 16, "bold"), width=300, height=50,
                      fg_color=self.colors["success"], hover_color="#009624").pack(pady=30)

    def save_theatre(self, popup):
        theatre_name = self.theatre_entry.get().strip()
        if not theatre_name:
            messagebox.showerror("Error", "Please enter a theatre name!")
            return

        if theatre_name in self.theatre_data["theatres"]:
            messagebox.showerror("Error", "Theatre already exists!")
            return

        self.theatre_data["theatres"][theatre_name] = []
        self.save_data()
        self.refresh_theatre_display()
        messagebox.showinfo("Success", f"Theatre '{theatre_name}' created!")
        # popup.destroy()

    def add_movie_popup(self):
        popup = self.create_popup("ADD MOVIE", "600x500")

        ctk.CTkLabel(popup, text="SELECT THEATRE:", font=("Arial", 20),
                     text_color=self.colors["accent"]).pack(pady=15)

        self.theatre_var = ctk.StringVar(value="Select Theatre")
        theatres = list(self.theatre_data["theatres"].keys())
        theatre_menu = ctk.CTkOptionMenu(popup, variable=self.theatre_var,
                                         values=theatres, font=("Arial", 18),
                                         width=400, height=50, dropdown_font=("Arial", 16))
        theatre_menu.pack(pady=10)

        ctk.CTkLabel(popup, text="MOVIE TITLE:", font=("Arial", 20),
                     text_color=self.colors["accent"]).pack(pady=15)

        self.movie_entry = ctk.CTkEntry(popup, placeholder_text="Enter movie title...",
                                        font=("Arial", 18), width=400, height=60,
                                        border_width=2, corner_radius=10)
        self.movie_entry.pack()

        ctk.CTkButton(popup, text="ADD MOVIE", command=lambda: self.save_movie(popup),
                      font=("Arial", 16, "bold"), width=300, height=50,
                      fg_color=self.colors["success"], hover_color="#009624").pack(pady=30)

    def save_movie(self, popup):
        theatre = self.theatre_var.get()
        movie = self.movie_entry.get().strip()

        if theatre == "Select Theatre":
            messagebox.showerror("Error", "Please select a theatre!")
            return

        if not movie:
            messagebox.showerror("Error", "Please enter a movie title!")
            return

        if movie in self.theatre_data["theatres"][theatre]:
            messagebox.showerror("Error", "Movie already exists in this theatre!")
            return

        self.theatre_data["theatres"][theatre].append(movie)
        self.save_data()
        self.refresh_theatre_display()
        messagebox.showinfo("Success", f"Movie '{movie}' added to {theatre}!")
        # popup.destroy()

    def delete_theatre_popup(self):
        popup = self.create_popup("DELETE THEATRE", "600x400")

        ctk.CTkLabel(popup, text="SELECT THEATRE TO DELETE:", font=("Arial", 20),
                     text_color=self.colors["accent"]).pack(pady=30)

        self.del_theatre_var = ctk.StringVar(value="Select Theatre")
        theatres = list(self.theatre_data["theatres"].keys())
        theatre_menu = ctk.CTkOptionMenu(popup, variable=self.del_theatre_var,
                                         values=theatres, font=("Arial", 18),
                                         width=400, height=50, dropdown_font=("Arial", 16))
        theatre_menu.pack()

        ctk.CTkButton(popup, text="CONFIRM DELETE", command=lambda: self.confirm_delete_theatre(popup),
                      font=("Arial", 16, "bold"), width=300, height=50,
                      fg_color=self.colors["danger"], hover_color="#b71c1c").pack(pady=30)

    def confirm_delete_theatre(self, popup):
        theatre = self.del_theatre_var.get()
        if theatre == "Select Theatre":
            messagebox.showerror("Error", "Please select a theatre!")
            return

        del self.theatre_data["theatres"][theatre]
        self.save_data()
        self.refresh_theatre_display()
        messagebox.showinfo("Success", f"Theatre '{theatre}' and all movies deleted!")
        # popup.destroy()

    def delete_movie_popup(self):
        popup = self.create_popup("🗑DELETE MOVIE", "600x500")

        ctk.CTkLabel(popup, text="SELECT THEATRE:", font=("Arial", 20),
                     text_color=self.colors["accent"]).pack(pady=15)

        self.del_movie_theatre_var = ctk.StringVar(value="Select Theatre")
        theatres = list(self.theatre_data["theatres"].keys())
        theatre_menu = ctk.CTkOptionMenu(popup, variable=self.del_movie_theatre_var,
                                         values=theatres, command=self.update_movie_list,
                                         font=("Arial", 18), width=400, height=50)
        theatre_menu.pack(pady=10)

        ctk.CTkLabel(popup, text="SELECT MOVIE:", font=("Arial", 20),
                     text_color=self.colors["accent"]).pack(pady=15)

        self.del_movie_var = ctk.StringVar(value="Select Movie")
        self.movie_menu = ctk.CTkOptionMenu(popup, variable=self.del_movie_var,
                                            values=[], font=("Arial", 18),
                                            width=400, height=50)
        self.movie_menu.pack(pady=10)

        ctk.CTkButton(popup, text="CONFIRM DELETE", command=lambda: self.confirm_delete_movie(popup),
                      font=("Arial", 16, "bold"), width=300, height=50,
                      fg_color=self.colors["danger"], hover_color="#b71c1c").pack(pady=30)

    def update_movie_list(self, choice):
        movies = self.theatre_data["theatres"][choice]
        self.movie_menu.configure(values=movies)
        self.del_movie_var.set("Select Movie")

    def confirm_delete_movie(self, popup):
        theatre = self.del_movie_theatre_var.get()
        movie = self.del_movie_var.get()

        if theatre == "Select Theatre" or movie == "Select Movie":
            messagebox.showerror("Error", "Please select both theatre and movie!")
            return

        self.theatre_data["theatres"][theatre].remove(movie)
        self.save_data()
        self.refresh_theatre_display()
        messagebox.showinfo("Success", f"Movie '{movie}' deleted from {theatre}!")
        # popup.destroy()


if __name__ == "__main__":
    AdminSystem()

