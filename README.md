TaskAPI
A FastAPI-based task management application for creating, managing, and tracking tasks efficiently.

Features
Task Management: Create, read, update, and delete tasks
FastAPI Framework: High-performance, modern Python web framework
Async Support: Asynchronous request handling for better performance
Interactive Documentation: Automatic API documentation with Swagger UI
Lifespan Events: Proper application startup and shutdown handling
Installation
Clone the repository:
bash
git clone https://github.com/Kanishkp2906/TaskAPI.git
cd TaskAPI
Create a virtual environment:
bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
Install dependencies:
bash
pip install -r requirements.txt
Usage
Start the development server:
bash
uvicorn main:app --reload
Access the application:
API: http://localhost:8000
Interactive API Documentation: http://localhost:8000/docs
Alternative Documentation: http://localhost:8000/redoc
API Endpoints
Method	Endpoint	Description
GET	/	Welcome message
GET	/tasks	Get all tasks
POST	/tasks	Create a new task
GET	/tasks/{id}	Get a specific task
PUT	/tasks/{id}	Update a task
DELETE	/tasks/{id}	Delete a task
Project Structure
TaskAPI/
├── main.py              # FastAPI application entry point
├── middleware/          # Custom middleware
│   └── log_events.py   # Logging middleware
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
Technologies Used
FastAPI: Modern, fast web framework for building APIs
Python 3.13: Latest Python version
Uvicorn: ASGI server for running the application
Pydantic: Data validation using Python type annotations
Development
Install development dependencies:
bash
pip install fastapi uvicorn python-multipart
Run with auto-reload:
bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Contributing
Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
Kanishk Patel - @Kanishkp2906

Project Link: https://github.com/Kanishkp2906/TaskAPI

