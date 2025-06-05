import json
from datetime import datetime
import uuid
import time
import threading
from queue import Queue
import logging
from typing import Optional, Dict, List
import random
from .api_manager import ResilientAPIClient


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hypothesis_generator.log'),
        logging.StreamHandler()
    ]
)

class HypothesisGenerator:
    def __init__(self, api_keys: List[str]):
        self.api_client = ResilientAPIClient(api_keys)
        self.hypotheses: Dict[str, dict] = {}
        self.generation_queue = Queue()
        self.is_processing = False
        self.processing_thread = None
        self.last_response = None
        self.consecutive_errors = 0
        self.last_statements = set()  # Track recent statements to avoid duplicates
        self.start_processing_thread()

    def start_processing_thread(self):
        """Start the background processing thread."""
        if not self.processing_thread or not self.processing_thread.is_alive():
            self.processing_thread = threading.Thread(target=self._process_queue, daemon=True)
            self.processing_thread.start()
            logging.info("Started background processing thread")

    def _process_queue(self):
        """Background thread to process the generation queue."""
        while True:
            try:
                if not self.generation_queue.empty():
                    self.is_processing = True
                    self._generate_next_hypothesis()
                else:
                    self.is_processing = False
                    time.sleep(2)  # Increased wait time between checks
            except Exception as e:
                logging.error(f"Error in processing thread: {str(e)}")
                self.consecutive_errors += 1
                wait_time = min(300, 2 ** self.consecutive_errors)  # Max 5 minutes
                time.sleep(wait_time)

    def _generate_next_hypothesis(self):
        """Generate the next hypothesis in the queue."""
        try:
            # Add randomization and delay
            time.sleep(random.uniform(3, 5))  # Random delay between 3-5 seconds
            
            # Create unique prompt with multiple random elements
            prompt = self._create_prompt()
            response = self.api_client.make_request(prompt)
            
            if response and 'candidates' in response:
                # Check if response is different from last one
                if response != self.last_response:
                    self.last_response = response
                    hypothesis = self._parse_response(response)
                    
                    if hypothesis and self._is_unique_statement(hypothesis['statement']):
                        self._save_hypothesis(hypothesis)
                        logging.info(f"Generated hypothesis: {hypothesis['id']}")
                        self.consecutive_errors = 0  # Reset error count on success
                        self.last_statements.add(hypothesis['statement'])
                        # Keep only last 10 statements to avoid memory growth
                        if len(self.last_statements) > 10:
                            self.last_statements.pop()
                    else:
                        logging.warning("Generated duplicate statement, retrying...")
                        self.consecutive_errors += 1
                        time.sleep(5)  # Wait before retry
                else:
                    logging.warning("Received duplicate response, retrying...")
                    self.consecutive_errors += 1
                    time.sleep(5)  # Wait before retry
            else:
                logging.error("Invalid response from API")
                self.consecutive_errors += 1
                
        except Exception as e:
            logging.error(f"Error generating hypothesis: {str(e)}")
            self.consecutive_errors += 1
        finally:
            # Add next generation to queue with delay based on error count
            wait_time = min(300, 2 ** self.consecutive_errors)  # Max 5 minutes
            time.sleep(wait_time)
            self.generation_queue.put(True)

    def _is_unique_statement(self, statement: str) -> bool:
        """Check if the statement is unique compared to recent ones."""
        # Normalize statement for comparison
        normalized = statement.lower().strip()
        return normalized not in {s.lower().strip() for s in self.last_statements}

    def generate_hypothesis(self) -> Optional[dict]:
        """Add a new hypothesis generation request to the queue."""
        if not self.is_processing:
            self.generation_queue.put(True)
            logging.info("Added new generation request to queue")
        return self.hypotheses.get(max(self.hypotheses.keys(), default=None))

    def _create_prompt(self) -> str:
        """Create the prompt for hypothesis generation."""
        # Add multiple random elements to prevent caching
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
            
        except Exception as e:
            logging.error(f"Error parsing response: {str(e)}")
            return None

    def _save_hypothesis(self, hypothesis: dict):
        """Save the hypothesis to a file."""
        try:
            with open('backend/hypotheses.txt', 'a') as f:
                f.write(json.dumps(hypothesis) + '\n')
        except Exception as e:
            logging.error(f"Error saving hypothesis: {str(e)}")

    def get_hypothesis(self, hypothesis_id: str) -> Optional[dict]:
        """Get a specific hypothesis by ID."""
        return self.hypotheses.get(hypothesis_id)

    def get_all_hypotheses(self):
        return list(self.hypotheses.values())

    def get_api_stats(self) -> Dict:
        """Get current API usage statistics."""
        return self.api_client.get_api_stats() 