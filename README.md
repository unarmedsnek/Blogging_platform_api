# Blogging Platform API

A REST API for a personal blogging platform built with Flask and SQLAlchemy.

Project from: https://roadmap.sh/projects/blogging-platform-api

## Requirements

- Python 3.10+

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/unarmedsnek/Blogging_platform_api.git
cd Blogging_platform_api
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv api_env
.\api_env\Scripts\activate

# Linux/macOS
python -m venv api_env
source api_env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /posts | Get all blog posts |
| GET | /posts/{id} | Get a single blog post |
| POST | /posts | Create a new blog post |
| PUT | /posts/{id} | Update a blog post |
| DELETE | /posts/{id} | Delete a blog post |
