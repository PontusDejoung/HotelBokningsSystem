# Hotel Reservation System

## Project Description
This project is a Flask-based hotel reservation system that manages customer registrations, room bookings, and invoice tracking using a MySQL database. The system provides functionalities for adding customers, booking rooms, modifying reservations, and handling invoices.

## Features
- Customer registration
- Hotel room management
- Room reservation with extra bed options
- Reservation cancellation and modification
- Invoice management

## Technologies Used
- **Flask** - Web framework for Python
- **Flask-SQLAlchemy** - ORM for database interactions
- **Flask-Migrate** - Handles database migrations
- **MySQL** - Relational database

## Installation and Setup
### Prerequisites
Ensure you have the following installed:
- Python 3
- MySQL
- Virtual environment (optional but recommended)

### Steps to Install and Run
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo.git
   cd your-repo
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your MySQL database in `app.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user:password@host/database'
   ```
   Replace `user`, `password`, `host`, and `database` with your actual MySQL credentials.

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
6. Run the application:
   ```bash
   python app.py
   ```

## Usage
Once the application is running, you can perform the following operations:
- **Register a Customer:** The application prompts for customer details.
- **Book a Room:** Specify room type, dates, and optional extra bed.
- **Cancel or Modify a Reservation:** Search by customer name, then cancel or change booking details.
- **Manage Invoices:** Track payments and update invoice status.

## File Structure
- `app.py` - Main Flask application containing models and functions.
- `migrations/` - Database migration files.
- `requirements.txt` - List of required dependencies.

---
This project is a simple reservation management system intended for learning purposes and can be expanded with additional features such as user authentication and a front-end interface.
