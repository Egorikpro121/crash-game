"""Task scheduler."""
import schedule
import time
from typing import Callable


class TaskScheduler:
    """Task scheduler for background jobs."""
    
    def __init__(self):
        """Initialize scheduler."""
        self.jobs = []
    
    def add_daily_task(self, task: Callable, time_str: str):
        """Add daily task."""
        schedule.every().day.at(time_str).do(task)
    
    def add_hourly_task(self, task: Callable):
        """Add hourly task."""
        schedule.every().hour.do(task)
    
    def add_minute_task(self, task: Callable, minutes: int = 1):
        """Add task every N minutes."""
        schedule.every(minutes).minutes.do(task)
    
    def run(self):
        """Run scheduler."""
        while True:
            schedule.run_pending()
            time.sleep(1)
