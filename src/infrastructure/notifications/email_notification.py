from src.application.common.notifications.interfaces import NotificationService


class EmailNotificationService(NotificationService):
    async def send_notification(self, destination: str, message: str) -> None:
        print(f"Sending email to {destination} with message: {message}")
