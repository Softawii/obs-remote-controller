import math

class PageSystem:    
    def __init__(self, emoji_list):
        self._current_page_number = 1
        self._current_page_items_number = len(emoji_list)
        self._max_items_per_page = len(emoji_list)
        self.emoji_list = emoji_list
        
    def get_current_page_items(self, scenes):
        
        last_page_size = len(scenes) % self._max_items_per_page
        last_page = math.ceil(len(scenes) / self._max_items_per_page)
        
        if last_page_size == 0 or self._current_page_number != last_page:
            self._current_page_items_number = self._max_items_per_page
        else:
            self._current_page_items_number = last_page_size
        
        start_index = (self._current_page_number - 1) * self._max_items_per_page
        return scenes[start_index:start_index + self._current_page_items_number]
    
    def set_page(self, page: int):
        self._current_page_number = page
        
    def get_current_page_items_number(self):
        return self._current_page_items_number