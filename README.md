# PhotoSphere 📸

PhotoSphere is a beautiful, responsive, full-stack photo gallery platform built with **Django** and styled with **Tailwind CSS**. It allows users to upload, categorize, and showcase their photography, while offering interactive social features like liking and commenting.

## ✨ Features

- **User Authentication**: Secure login and registration with visually stunning, glassmorphism-themed auth pages.
- **Dynamic Photo Gallery**: 
  - Browse photos beautifully arranged by categories (Nature, Wildlife, Portrait, Architecture, Street, Abstract).
  - Horizontal scrolling rows with interactive sliders.
- **Interactive Modals**: Click on any photo to open a high-resolution cinematic modal that displays the image alongside its details, likes, and live comments.
- **Social Features**:
  - **Asynchronous Likes**: Users can like photos seamlessly without page reloads.
  - **Live Commenting**: Instantly post and view comments on any photo.
- **Modern UI/UX**:
  - Sleek, soft pastel gradient backgrounds with animated floating orbs.
  - Responsive design that looks great on mobile, tablet, and desktop devices.
- **Photo Uploads**: An intuitive "Add Photo" interface featuring live image previews before submission.

## 🛠️ Technology Stack

- **Backend**: Python, Django
- **Frontend**: HTML5, Tailwind CSS (via django-tailwind), Vanilla JavaScript
- **Database**: SQLite (Development)
- **Deployment Ready**: Configured with `gunicorn` and `requirements.txt` for easy deployment to platforms like Render, Heroku, or Railway.

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites
- Python 3.8+
- Node.js (for Tailwind CSS processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/PhotoSphere.git
   cd PhotoSphere
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Tailwind CSS**
   ```bash
   python manage.py tailwind install
   ```

5. **Apply Database Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser** (to access the admin panel)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   You'll need two terminal windows:
   - *Terminal 1 (Django Server):*
     ```bash
     python manage.py runserver
     ```
   - *Terminal 2 (Tailwind Compiler):*
     ```bash
     python manage.py tailwind start
     ```

## 📂 Project Structure

- `PhotoSphere/` - The core Django project settings and WSGI configuration.
- `PhotoApp/` - The main application containing the models (Photo, Category, Like, Comment), views, and URLs.
- `templates/` - Contains all HTML templates, including the layout and application-specific pages.
- `theme/` - The django-tailwind application that manages the Tailwind CSS configuration and assets.
- `media/` - Local storage directory for user-uploaded photos.

## 🚢 Deployment

This project is configured for easy deployment:
- A `Procfile` is included for PaaS providers (uses `gunicorn`).
- `requirements.txt` is fully populated.
- **Note**: Before deploying to production, ensure you configure environment variables for `SECRET_KEY`, `DEBUG=False`, and update `ALLOWED_HOSTS`. You will also need to configure a production database (like PostgreSQL) and a static/media file hosting solution (like WhiteNoise or AWS S3).

## 📄 License

This project is open-source and available under the MIT License.
