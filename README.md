
# API Project Documentation

## Overview
This API is built with **FastAPI** to manage authentication and perform operations with Google Drive. It includes login functionality, file listing from Google Drive, and uses JWT tokens for secure authentication.

---

## Requirements

- Python 3.11
- FastAPI
- Uvicorn
- Python-dotenv
- Google-auth libraries

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd api_project
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3.11 -m venv venv
   .\venv\Scripts\Activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install fastapi uvicorn python-dotenv google-auth google-auth-oauthlib google-api-python-client
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory with the following:
   ```
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

---

## Run the Application

Start the server using Uvicorn:
```bash
.\venv\Scripts\Activate
uvicorn app.main:app --reload
```

The API will be accessible at `http://localhost:8000`.

---

## Features

### Authentication
- **Login Endpoint**: `/auth/login`
  - Accepts `username` and `password` using `OAuth2PasswordRequestForm`.
  - Returns a JWT token.

### Google Drive Integration
- **Authorize**: `/drive/authorize`
  - Redirects the user to the Google authentication page.
- **Callback**: `/drive/oauth2callback`
  - Handles the OAuth2 callback.
- **List Files**: `/drive/files`
  - Lists the user’s Google Drive files.

### Example Endpoint
- `/hello`: Returns a simple JSON response: `{"message": "Hello World"}`.

---

## Project Structure

```
api_project/
├── app/
│   ├── main.py                 # Entry point for the API
│   ├── core/
│   │   ├── config.py           # Configuration and environment variables
│   │   ├── security.py         # Security-related utilities
│   ├── models/
│   │   ├── user.py             # User models
│   ├── routers/
│   │   ├── auth.py             # Authentication routes
│   │   ├── drive.py            # Google Drive routes
│   ├── schemas/
│   │   ├── user.py             # Data validation for users
│   │   ├── drive.py            # Data validation for Drive operations
│   ├── services/
│   │   ├── auth.py             # Token generation and verification
│   │   ├── google_drive.py     # Google Drive API interactions
│   ├── utils/
│   │   ├── helpers.py          # Helper utilities
```

---

## Testing

- Access Swagger UI documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Use ReDoc for API visualization: [http://localhost:8000/redoc](http://localhost:8000/redoc)
