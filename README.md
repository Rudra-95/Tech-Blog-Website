# The Phenomenal Achiever - Blog
Welcome to **The Phenomenal Achiever** repository! This is a simple blog application built using Flask, HTML, CSS, and Bootstrap for the front-end. The blog is designed to allow users to read posts, and administrators to manage posts (create, edit, and delete) through an easy-to-use admin dashboard.

## Features
- **Admin Dashboard**: Allows the administrator to manage posts (add, edit, delete).
- **User Posts**: Users can read blog posts and view the details.
- **Image Upload**: Admins can upload images while creating or editing posts.
- **Responsive UI**: Built using Bootstrap for a clean and responsive design.

## Tech Stack
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (or your chosen database)
- **Deployment**: (e.g., Heroku, AWS, or local server)

### Prerequisites
1. Python 3.x
2. Git

### Steps
1. Clone the repository
2. Create a virtual-environment (optional)
3. Install the dependencies (pip install -r requirements.txt)
4. Run the Flask app & the program written in it
5. Visit the link to the browser froom the output

File-Structure
----------------------
/phenomenal-achiever
├── app.py                  # Flask app logic
├── /templates              # HTML files
│   ├── index.html          # Home page
│   ├── about.html          # About page
│   ├── contact.html        # Contact page
│   ├── dashboard.html      # Admin dashboard
│   └── edit.html           # Edit post page
├── /static                 # Static files (CSS, images, JavaScript)
│   ├── /img                # Image files
│   └── /css                # CSS files
├── /models                 # Models for database (e.g., Post)
├── requirements.txt        # Python dependencies
└── README.md               # This file
