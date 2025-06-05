import json
import uuid
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import requests
from dataclasses import dataclass


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
                self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
                if self.current_key_index == start_index:
                    return None
                continue
            
            # Key is available
            return key_status.key

    def mark_key_failure(self, key: str, error_type: str):
        """Mark a key as failed and update its status."""
        if key in self.api_keys:
            status = self.api_keys[key]
            status.failures += 1
            
            if error_type == "RATE_LIMIT":
                status.cooldown_until = datetime.now() + self.cooldown_period
            elif error_type == "QUOTA_EXCEEDED":
                status.cooldown_until = datetime.now() + timedelta(hours=24)
            elif status.failures >= self.max_failures:
                status.cooldown_until = datetime.now() + self.cooldown_period

    def mark_key_success(self, key: str):
        """Mark a key as successful and reset its failure count."""
        if key in self.api_keys:
            status = self.api_keys[key]
            status.failures = 0
            status.successful_requests += 1
            status.total_requests += 1
            status.last_used = datetime.now()

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
                key[:8] + "...": {
                    "failures": status.failures,
                    "total_requests": status.total_requests,
                    "successful_requests": status.successful_requests,
                    "success_rate": round(status.successful_requests / status.total_requests * 100, 2) if status.total_requests > 0 else 0,
                    "in_cooldown": bool(status.cooldown_until and datetime.now() < status.cooldown_until),
                    "cooldown_remaining": str((status.cooldown_until - datetime.now()).total_seconds() // 60) + " minutes" 
                        if (status.cooldown_until and datetime.now() < status.cooldown_until) else "None"
                } for key, status in self.api_keys.items()
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

                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    self.api_manager.mark_key_success(key)
                    return response_data
                
                elif response.status_code == 429:
                    self.api_manager.mark_key_failure(key, "RATE_LIMIT")
                
                elif response.status_code == 401:
                    self.api_manager.mark_key_failure(key, "UNAUTHORIZED")
                
                elif response.status_code >= 500:
                    self.api_manager.mark_key_failure(key, "SERVER_ERROR")
                
                else:
                    self.api_manager.mark_key_failure(key, "UNKNOWN")

            except requests.Timeout:
                self.api_manager.mark_key_failure(key, "TIMEOUT")
            
            except requests.RequestException:
                self.api_manager.mark_key_failure(key, "NETWORK_ERROR")
            
            except Exception:
                self.api_manager.mark_key_failure(key, "UNKNOWN")

            time.sleep(self.api_manager.retry_delay)
            retries += 1

        return None

    def get_api_stats(self) -> Dict:
        """Get current API usage statistics."""
        return self.api_manager.get_key_stats()


class HypothesisGenerator:
    def __init__(self, api_keys: List[str]):
        self.api_client = ResilientAPIClient(api_keys)
        self.hypotheses: Dict[str, dict] = {}
        self.last_statements = set()  # Track recent statements to avoid duplicates

    def _create_prompt(self) -> str:
        """Create the prompt for hypothesis generation."""
        # Add multiple random elements to prevent caching
        import random
        random_seed = random.randint(1, 1000)
        timestamp = datetime.now().isoformat()
        random_context = random.choice([
            "scientific research",
            "experimental analysis",
            "empirical study",
            "theoretical framework",
            "research methodology"
        ])
        
        return f"""Generate a unique scientific hypothesis with the following structure (Seed: {random_seed}, Context: {random_context}, Time: {timestamp}):
        1. A clear, testable statement that hasn't been generated before
        2. Background information and context
        3. Expected outcomes if the hypothesis is true
        4. Potential implications and applications

        Format the response as a JSON object with these fields:
        - statement: The main hypothesis (must be unique)
        - background: Context and reasoning
        - expected_outcomes: List of expected results
        - implications: List of potential impacts"""

    def _parse_response(self, response: dict) -> Optional[dict]:
        """Parse the API response into a hypothesis object."""
        try:
            content = response['candidates'][0]['content']['parts'][0]['text']
            # Clean the response text by removing markdown code block markers
            if content.startswith('```json'):
                content = content[7:]  # Remove ```json
            if content.endswith('```'):
                content = content[:-3]  # Remove ```
            content = content.strip()
            
            data = json.loads(content)
            
            hypothesis = {
                'id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat(),
                'statement': data.get('statement', ''),
                'background': data.get('background', ''),
                'expected_outcomes': data.get('expected_outcomes', []),
                'implications': data.get('implications', [])
            }
            
            self.hypotheses[hypothesis['id']] = hypothesis
            return hypothesis
            
        except Exception:
            return None

    def _is_unique_statement(self, statement: str) -> bool:
        """Check if the statement is unique compared to recent ones."""
        # Normalize statement for comparison
        normalized = statement.lower().strip()
        return normalized not in {s.lower().strip() for s in self.last_statements}

    def generate_hypothesis(self, api_keys: List[str]) -> Dict[str, Any]:
        """Generate a new scientific hypothesis."""
        # Initialize with provided API keys
        self.api_client = ResilientAPIClient(api_keys)
        
        # Create prompt and make API request
        prompt = self._create_prompt()
        response = self.api_client.make_request(prompt)
        
        if response and 'candidates' in response:
            hypothesis = self._parse_response(response)
            
            if hypothesis and self._is_unique_statement(hypothesis['statement']):
                # Track this statement to avoid duplicates in future
                if len(self.last_statements) >= 10:
                    self.last_statements.pop()
                self.last_statements.add(hypothesis['statement'])
                
                return hypothesis
        
        # Return error information if generation failed
        return {
            "error": True,
            "message": "Failed to generate hypothesis"
        }

    def get_api_stats(self) -> Dict:
        """Get current API usage statistics."""
        return self.api_client.get_api_stats()


def run_genethink_ai(api_keys: List[str]) -> Dict[str, Any]:
    """
    Main entry point for the Genethink AI plugin.
    
    This function generates a scientific hypothesis using the Gemini AI model.
    
    Args:
        api_keys: List of Gemini API keys to use for hypothesis generation
        
    Returns:
        A dictionary containing either the generated hypothesis or error information
    """
    try:
        # Initialize the hypothesis generator
        generator = HypothesisGenerator(api_keys)
        
        # Generate a new hypothesis
        result = generator.generate_hypothesis(api_keys)
        
        # Add API stats to the result
        result["api_stats"] = generator.get_api_stats()
        
        return result
    
    except Exception as e:
        return {
            "error": True,
            "message": f"Error in Genethink AI plugin: {str(e)}"
        }
