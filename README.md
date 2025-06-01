# ApnaMovieTicketBookingSystem - Movie Ticket Booking & Validation System
<!-- Replace with actual screenshot -->
ApnaMovieTicketBookingSystem is a comprehensive movie ticket booking system with QR code validation capabilities. It consists of two main applications:
1. **Booking System**: For users to select movies, choose seats, and receive tickets via email
2. **Validator App**: For theater staff to scan and validate tickets using a webcam

## Features

### Booking System
- 🎬 Theater and movie selection
- 🪑 Interactive seat map with visual booking status
- 📝 Personal details collection
- 📧 Email delivery with QR code tickets
- 🔁 Multi-booking support
- 🎨 Modern dark-themed UI with customtkinter

### Validator App
- 📷 Live webcam QR code scanning
- 🎫 Real-time ticket validation
- 📊 Detailed ticket information display
- ❌ Mark tickets as used
- 💡 User-friendly interface

## Installation

### Prerequisites
- Python 3.7+
- Pip package manager

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ApnaMovieTicketBookingSystem.git
   cd ApnaMovieTicketBookingSystem 
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure email settings:
   - Create a `config.json` file with your email credentials:
     ```json
     {
       "sender_email": "your_email@example.com",
       "sender_password": "your_app_password",
       "smtp_server": "smtp.example.com",
       "smtp_port": 587
     }
     ```

4. Set up theater data:
   - Create a `data.json` file with theater information:
     ```json
     {
       "theatres": {
         "Theater 1": ["Movie A", "Movie B"],
         "Theater 2": ["Movie C", "Movie D"]
       }
     }
     ```

## Usage

### Running the Booking System
```bash
python booking_system.py
```

### Running the Validator
```bash
python validator.py
```

### Booking Process
1. Select a theater from the list
2. Choose a movie
3. Select available seats (up to 20 seats)
4. Enter personal details (name and email)
5. Confirm booking to receive tickets via email

### Validation Process
1. Launch the validator app
2. Click "Start Scanning" to activate webcam
3. Hold ticket QR code in front of camera
4. View ticket details and validity status
5. Click "Mark as Used" to invalidate ticket

## File Structure
```plaintext
ApnaMovieTicketBookingSystem/
├── booking_system.py        # Main booking application
├── validator.py             # Ticket validation application
├── data.json                # Theater and movie data
├── config.json              # Email configuration
├── bookings.json            # Database of all bookings
├── qrcodes/                 # Generated QR code images
├── requirements.txt         # Python dependencies
└── README.md                # This documentation
```

## Dependencies
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI toolkit
- [OpenCV](https://opencv.org/) - Computer vision for QR scanning
- [pyzbar](https://pypi.org/project/pyzbar/) - QR code decoding
- [qrcode](https://pypi.org/project/qrcode/) - QR code generation
- [Pillow](https://python-pillow.org/) - Image processing

## Configuration Options
- **Email Settings**: Modify `config.json` to use your SMTP server
- **Theater Data**: Update `data.json` with current theaters and movies
- **UI Themes**: Adjust colors in the `colors` dictionary
- **Ticket Pricing**: Modify price calculation in `confirm_booking()` method

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request



## Support
For issues or feature requests, please [open an issue](https://github.com/yourusername/fastticket/issues).

---

**Note**: For production use:
1. Replace placeholder email credentials with actual values
2. Implement proper security measures for sensitive data
3. Add error handling for edge cases
4. Consider using a database instead of JSON files for scalability
