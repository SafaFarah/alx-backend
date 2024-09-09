#!/usr/bin/python3
""" module that inherits from BaseCaching and implements LFU caching """
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFU Caching System """

    def __init__(self):
        """ Initialize the class """
        super().__init__()
        self.freq = {}
        self.use_order = []

    def put(self, key, item):
        """ Add an item in the cache
        If the cache is full, discard the least frequently used item
        If multiple items have the same frequency, discard the lru
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq[key] += 1
            self.use_order.remove(key)
            self.use_order.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_freq = min(self.freq.values())
                lfu_keys = ([k for k in self.use_order
                            if self.freq[k] == min_freq])
                key_to_discard = lfu_keys[0]
                self.use_order.remove(key_to_discard)
                del self.cache_data[key_to_discard]
                del self.freq[key_to_discard]
                print(f"DISCARD: {key_to_discard}")
            self.cache_data[key] = item
            self.freq[key] = 1
            self.use_order.append(key)

    def get(self, key):
        """ Retrieve an item by key. Update frequency and usage order """
        if key is None or key not in self.cache_data:
            return None
        self.freq[key] += 1
        self.use_order.remove(key)
        self.use_order.append(key)
        return self.cache_data[key]
