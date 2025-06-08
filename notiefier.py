from plyer import notification
import threading
import settings

def start_notifications(title, message):
    def show_notification():
            notification.notify(
                title=title,
                message=message,
                app_icon = settings.PROGRAM_ICON,
                timeout=2  )

    threading.Thread(target=show_notification, daemon=True).start()
