class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

#Class for the Observer Method
class Observer:
    def update(self, message):
        pass


class NotificationObserver(Observer):
    def __init__(self, user_id):
        self.user_id = user_id

    def update(self, message):
        from models import Notification, db
        # Create a new notification in the database
        notification = Notification(user_id=self.user_id, message=message)
        db.session.add(notification)
        db.session.commit()
