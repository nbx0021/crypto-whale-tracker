# producer/fx_rate.py
import requests
import time
import logging
from typing import Optional

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("FXRateCache")

class FXRateCache:
    def __init__(self, cache_ttl_seconds: int = 3600) -> None:
        self.rate: Optional[float] = None
        self.last_update: float = 0.0
        self.ttl: int = cache_ttl_seconds  # Refreshes every 1 hour
        self.api_url: str = "https://open.er-api.com/v6/latest/USD"

    def get_usd_to_inr(self) -> float:
        current_time = time.time()
        
        # If the cache is empty or expired, fetch a fresh dynamic rate
        if self.rate is None or (current_time - self.last_update > self.ttl):
            try:
                response = requests.get(self.api_url, timeout=10)
                response.raise_for_status()
                data = response.json()
                self.rate = float(data['rates']['INR'])
                self.last_update = current_time
                logger.info(f"🔄 Fetched fresh USD-to-INR rate: ₹{self.rate:.2f}")
            except Exception as e:
                logger.error(f"⚠️ Failed to fetch FX rate: {e}")
                # Fallback so the streaming pipeline doesn't crash if the API drops
                if self.rate is None:
                    self.rate = 87.00
                    logger.warning(f"⚠️ Using fallback FX rate: ₹{self.rate:.2f}")
                    
        return self.rate

# Instantiate a single global cache object to be used by the fetcher
fx_cache = FXRateCache()