from collections import defaultdict, deque
from typing import List, Dict
from config import MAX_HISTORY

class ConversationMemory:
    def __init__(self, max_history: int = MAX_HISTORY):
        # Maps chat_id -> deque of message dicts (role, content)
        self.store = defaultdict(lambda: deque(maxlen=max_history))

    def add_message(self, chat_id: int, role: str, content: str) -> None:
        self.store[chat_id].append({"role": role, "content": content})

    def get_history(self, chat_id: int) -> List[Dict[str, str]]:
        return list(self.store[chat_id])

    def clear_history(self, chat_id: int) -> None:
        if chat_id in self.store:
            self.store[chat_id].clear()
