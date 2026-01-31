from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time as datetime_time
from plyer import notification

class NotificationScheduler:
    def __init__(self, callback):
        self.scheduler = BackgroundScheduler()
        self.callback = callback
        self.notification_time = "21:00"  # Default 9 PM
    
    def set_notification_time(self, time_str):
        """Set the daily notification time (format: HH:MM)"""
        self.notification_time = time_str
        self.reschedule()
    
    def start(self, notification_time="21:00"):
        """Start the scheduler with daily notifications"""
        self.notification_time = notification_time
        
        # Parse time
        hour, minute = map(int, self.notification_time.split(':'))
        
        # Schedule daily notification
        self.scheduler.add_job(
            self._send_notification,
            'cron',
            hour=hour,
            minute=minute,
            id='daily_journal_reminder'
        )
        
        self.scheduler.start()
    
    def _send_notification(self):
        """Send notification and trigger callback"""
        try:
            notification.notify(
                title='Journal Time! 📝',
                message='Time to reflect on your day',
                app_name='Journal Buddy',
                timeout=10
            )
            
            # Call the callback (opens the chat window)
            self.callback()
            
        except Exception as e:
            print(f"Notification error: {e}")
    
    def reschedule(self):
        """Reschedule the notification with new time"""
        if self.scheduler.running:
            self.scheduler.remove_job('daily_journal_reminder')
            hour, minute = map(int, self.notification_time.split(':'))
            self.scheduler.add_job(
                self._send_notification,
                'cron',
                hour=hour,
                minute=minute,
                id='daily_journal_reminder'
            )
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
    
    def trigger_now(self):
        """Manually trigger notification (for testing)"""
        self._send_notification()
