class SingletonSession:
    """Singleton class for managing user sessions."""
    _instance = None
    _user = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonSession, cls).__new__(cls)
        return cls._instance
#Sets, gets, and clears user statements
    def set_user(self, user):
        self._user = user

    def get_user(self):
        return self._user

    def clear_user(self):
        self._user = None
