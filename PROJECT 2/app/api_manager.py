import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from dataclasses import dataclass
import json

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more details
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('api_manager.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class APIKeyStatus:
    key: str
    last_used: datetime
    failures: int
    cooldown_until: Optional[datetime] = None
    total_requests: int = 0
    successful_requests: int = 0

class APIManager:
    def __init__(self, api_keys: List[str]):
        self.api_keys: Dict[str, APIKeyStatus] = {
            key: APIKeyStatus(key=key, last_used=datetime.min, failures=0)
            for key in api_keys
        }
        self.current_key_index = 0
        self.cooldown_period = timedelta(minutes=10)
        self.max_failures = 3
        self.retry_delay = 1  # seconds

    def get_next_available_key(self) -> Optional[str]:
        """Get the next available API key that's not in cooldown."""
        start_index = self.current_key_index
        while True:
            key_status = list(self.api_keys.values())[self.current_key_index]
            
            # Check if key is in cooldown
            if key_status.cooldown_until and datetime.now() < key_status.cooldown_until:
                logging.debug(f"Key {key_status.key[:8]}... is in cooldown until {key_status.cooldown_until}")
                self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
                if self.current_key_index == start_index:
                    logging.warning("All keys are in cooldown!")
                    return None
                continue
            
            # Key is available
            logging.debug(f"Using key {key_status.key[:8]}...")
            return key_status.key

    def mark_key_failure(self, key: str, error_type: str):
        """Mark a key as failed and update its status."""
        if key in self.api_keys:
            status = self.api_keys[key]
            status.failures += 1
            
            if error_type == "RATE_LIMIT":
                status.cooldown_until = datetime.now() + self.cooldown_period
                logging.warning(f"Key {key[:8]}... rate limited. Cooldown until {status.cooldown_until}")
            elif error_type == "QUOTA_EXCEEDED":
                status.cooldown_until = datetime.now() + timedelta(hours=24)
                logging.warning(f"Key {key[:8]}... quota exceeded. Cooldown for 24 hours")
            elif status.failures >= self.max_failures:
                status.cooldown_until = datetime.now() + self.cooldown_period
                logging.warning(f"Key {key[:8]}... exceeded max failures. Cooldown until {status.cooldown_until}")

    def mark_key_success(self, key: str):
        """Mark a key as successful and reset its failure count."""
        if key in self.api_keys:
            status = self.api_keys[key]
            status.failures = 0
            status.successful_requests += 1
            status.total_requests += 1
            status.last_used = datetime.now()
            logging.info(f"Key {key[:8]}... request successful. Total requests: {status.total_requests}")

    def get_key_stats(self) -> Dict:
        """Get statistics about API key usage."""
        total_keys = len(self.api_keys)
        available_keys = sum(1 for status in self.api_keys.values() 
                           if not status.cooldown_until or datetime.now() >= status.cooldown_until)
        
        return {
            "total_keys": total_keys,
            "available_keys": available_keys,
            "unavailable_keys": total_keys - available_keys,
            "key_details": {
                key: {
                    "failures": status.failures,
                    "success_rate": (status.successful_requests / status.total_requests * 100) 
                        if status.total_requests > 0 else 0,
                    "in_cooldown": bool(status.cooldown_until and datetime.now() < status.cooldown_until)
                }
                for key, status in self.api_keys.items()
            }
        }

class ResilientAPIClient:
    def __init__(self, api_keys: List[str]):
        self.api_manager = APIManager(api_keys)
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.max_retries = 3

    def make_request(self, prompt: str) -> Optional[dict]:
        """Make a resilient API request with automatic key rotation."""
        retries = 0
        while retries < self.max_retries:
            key = self.api_manager.get_next_available_key()
            if not key:
                logging.error("No available API keys!")
                time.sleep(self.api_manager.retry_delay)
                retries += 1
                continue

            try:
                headers = {
                    "Content-Type": "application/json",
                    "x-goog-api-key": key
                }
                
                data = {
                    "model": "gemini-2.0-flash",
                    "contents": [{
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }],
                    "safety_settings": [
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
                    ]
                }

                logging.debug(f"Sending request to Gemini API with key {key[:8]}...")
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=data,
                    timeout=30
                )

                logging.debug(f"Response status: {response.status_code}")
                logging.debug(f"Response headers: {response.headers}")
                
                if response.status_code == 200:
                    response_data = response.json()
                    logging.debug(f"Response data: {json.dumps(response_data, indent=2)}")
                    self.api_manager.mark_key_success(key)
                    return response_data
                
                elif response.status_code == 429:
                    self.api_manager.mark_key_failure(key, "RATE_LIMIT")
                    logging.warning(f"Rate limit exceeded for key {key[:8]}... Response: {response.text}")
                
                elif response.status_code == 401:
                    self.api_manager.mark_key_failure(key, "UNAUTHORIZED")
                    logging.error(f"Unauthorized key {key[:8]}... Response: {response.text}")
                
                elif response.status_code >= 500:
                    self.api_manager.mark_key_failure(key, "SERVER_ERROR")
                    logging.error(f"Server error with key {key[:8]}... Response: {response.text}")
                
                else:
                    self.api_manager.mark_key_failure(key, "UNKNOWN")
                    logging.error(f"Unknown error with key {key[:8]}... Status: {response.status_code}, Response: {response.text}")

            except requests.Timeout:
                self.api_manager.mark_key_failure(key, "TIMEOUT")
                logging.warning(f"Timeout with key {key[:8]}...")
            
            except requests.RequestException as e:
                self.api_manager.mark_key_failure(key, "NETWORK_ERROR")
                logging.error(f"Network error with key {key[:8]}...: {str(e)}")
            
            except Exception as e:
                self.api_manager.mark_key_failure(key, "UNKNOWN")
                logging.error(f"Unexpected error with key {key[:8]}...: {str(e)}")

            time.sleep(self.api_manager.retry_delay)
            retries += 1

        logging.error("All retries exhausted!")
        return None

    def get_api_stats(self) -> Dict:
        """Get current API usage statistics."""
        return self.api_manager.get_key_stats() 