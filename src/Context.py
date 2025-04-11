class Context:
    def __init__(self):
        self.context = []

    def add_context(self, last_cmnd):
        """Adds a new context to the list."""
        if len(self.context) == 1:
            self.clear_context()
        self.context.append(last_cmnd)

    def clear_context(self):
        """Clears the context list."""
        self.context = []

    def get_context(self):
        """Returns the current context as a string."""
        return self.context[0] if self.context else ""