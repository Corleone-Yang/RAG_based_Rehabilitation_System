from datetime import datetime, timedelta

# short term memory will keep items for 10 days
class short_term_memory:
    def __init__(self):
        self.memory = []
        self.memory_duration = timedelta(days=10)

    def remember(self, item):
        expiration_time = datetime.now() + self.memory_duration
        timestamped_item = (item, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), expiration_time)
        self.memory.append(timestamped_item)
        self._clean_memory()
    
    def _clean_memory(self):
        self.memory = [item for item in self.memory if datetime.now() < item[2]]

    def recall(self):
        self._clean_memory()  # Ensure memory is cleaned before recall
        return [(item, timestamp) for item, timestamp, _ in self.memory]

# long term memory will keep items forever
class long_term_memory:
    def __init__(self):
        self.memory = []
    
    def remember(self, item):
        self.memory.append(item)

    def recall(self):
        return self.memory

# dynamic memory will keep 15 items
class dynamic_memory:
    def __init__(self):
        self.memory = []
        self.memory_size = 15

    def remember(self, item):
        timestamped_item = (item, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.memory.append(timestamped_item)
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)

    def recall(self):
        return self.memory