from app import create_app
from app.scheduler import start_scheduler

app = create_app()

if __name__ == "__main__":
    scheduler = start_scheduler(app)
    app.run(debug=True)
