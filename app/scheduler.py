from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app

def start_scheduler(app):
    """Start the job scheduler for periodic processing of test cases."""
    scheduler = BackgroundScheduler()
    
    def trigger_endpoint():
        with app.app_context():
            current_app.test_client().post('/trigger')

    scheduler.add_job(trigger_endpoint, 'interval', seconds=86400)  # Runs every 24 hours
    scheduler.start()
    return scheduler
