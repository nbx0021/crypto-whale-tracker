# producer/fx_rate.py
import requests
import time

class FXRateCache:
    def __init__(self, cache_ttl_seconds=3600):
        self.rate = None
        self.last_update = 0
        self.ttl = cache_ttl_seconds # Refreshes every 1 hour
        self.api_url = "https://open.er-api.com/v6/latest/USD"

    def get_usd_to_inr(self):
        current_time = time.time()
        
        # If the cache is empty or expired, fetch a fresh dynamic rate
        if self.rate is None or (current_time - self.last_update > self.ttl):
            try:
                response = requests.get(self.api_url)
                response.raise_for_status()
                data = response.json()
                self.rate = data['rates']['INR']
                self.last_update = current_time
                print(f"🔄 [System] Fetched fresh USD-to-INR rate: ₹{self.rate}")
            except Exception as e:
                print(f"⚠️ [Error] Failed to fetch FX rate: {e}")
                # Fallback so the streaming pipeline doesn't crash if the API drops
                if self.rate is None:
                    self.rate = 87.00 
                    
        return self.rate

# Instantiate a single global cache object to be used by the fetcher
fx_cache = FXRateCache()