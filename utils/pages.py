import math

class PageSystem:    
    def __init__(self, emoji_list, back_emoji, next_emoji):
        self._current_page_number = 1
        self._current_page_items_number = len(emoji_list)
        self._max_items_per_page = len(emoji_list)
        self.emoji_list = emoji_list
        self.back_emoji = back_emoji
        self.next_emoji = next_emoji
        self.scenes = []
        self.last_page = 0
        
    def get_current_page_items(self, scenes):
        
        self.scenes = scenes
        last_page_size = len(scenes) % self._max_items_per_page
        last_page = math.ceil(len(scenes) / self._max_items_per_page)
        self.last_page = last_page
        
        if last_page_size == 0 or self._current_page_number != last_page:
            self._current_page_items_number = self._max_items_per_page
        else:
            self._current_page_items_number = last_page_size
        
        start_index = (self._current_page_number - 1) * self._max_items_per_page
        return scenes[start_index:start_index + self._current_page_items_number]
    
    def set_page(self, page: int):
        self._current_page_number = page
        
    def increase_page(self):
        if self._current_page_number != self.last_page:
            self._current_page_number += 1
    
    def decrease_page(self):
        if self._current_page_number != 1:
            self._current_page_number -= 1
        
    def get_current_page_items_number(self):
        return self._current_page_items_number