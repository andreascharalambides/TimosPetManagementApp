# Pet Management Application

A Django-based web application that allows users to manage their pets, tasks, and reminders. Users can register, log in,
add pets, create tasks associated with their pets, and set reminders for various activities.

## Features

- **User Authentication**: Register, log in, and log out functionality.
- **Pet Management**: Add, view, and manage pets, including uploading photos.
- **Task Management**: Create tasks for pets with categories, start and end dates, and frequency.
- **Default Categories**: Automatically create default categories for new users.
- **Admin Interface**: Manage users, pets, tasks, and categories via Django admin.

## Prerequisites

- **Python 3.6+**
- **Django 3.x or 4.x**
- **Virtual Environment (Recommended)**

## Installation

### **1. Clone the Repository**

```bash
git clone https://github.com/yourusername/PetManagementApp.git
cd PetManagementApp
```

### **2. Create and Activate a Virtual Environment**

**For Windows:**

```bash
python -m venv env
env\Scripts\activate
```

**For macOS/Linux:**

```bash
python3 -m venv env
source env/bin/activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Apply Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

### **5. Create a Superuser**

```bash
python manage.py createsuperuser
```

### **6. Run the Development Server**

```bash
python manage.py runserver
```

### **7. Access the Application**

- **Open your web browser and go to http://localhost:8000/.**

### **8. Collecting Static Files for Production**

**Run the following command every time you update your static files:**

```bash
python manage.py collectstatic
```

## Usage

- **Register:** Navigate to /users/register/ to create a new account.
- **Log In:** Navigate to /users/login/ to log in.
- **Add Pets:** After logging in, add your pets by clicking on "Add a new pet."
- **Create Tasks:** Add tasks for your pets by clicking on "Add a new task."
- **View Pets and Tasks:** View your pets and their associated tasks on the home page.