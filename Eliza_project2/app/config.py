"""
Secure configuration file for API keys and settings.
DO NOT COMMIT THIS FILE TO VERSION CONTROL.
"""

# Gemini API Keys
GEMINI_API_KEYS = [
    "AIzaSyB84IDnLHw695xY3LSruiHvW3e18QE-q-A",
    "AIzaSyBBTgtN0FIKccxJLGRzmUkKhPQRT3xcCK8",
    "AIzaSyDbfmgqkIZ_NnZI3OajDDUpjvgHXaFqb6E",
    "AIzaSyAFv6bTyHrjHVhLzrK867mVzqbTwBx73JE",
    "AIzaSyCGfzbsdEzLscQD-fN2wZ3aAZJ52LLWHzc",
    "AIzaSyCVGkHG-eTP6Jh5oB4bMFrIsU4-QNfuG30",
    "AIzaSyB9paw2cIk04NnORpHy4A326ePjZEVnFmI",
    "AIzaSyCCMcuiVaiO2ZOLvSH8qmZrAYBXVU5II8s",
    "AIzaSyAvruSIYcraJqve9hr8mRbXxhyi1C0RaL4",
    "AIzaSyDBLPmSFGF1tay6z3e9ibDUnUAs2pT-4_w",
    "AIzaSyAqW54VUCiyqlu8JHN9bv-OMA1TRXeWqkY",
    "AIzaSyBmcuMde3qOd-CxBXsAK27YvjqG8vLzqso",
    "AIzaSyAekSqXWyr1CxbEPcSvcoGxB2OhFCapYi0",
    "AIzaSyD5bR1eSFNbnqZdnPJ3tc537XaFbQvIYBI",
    "AIzaSyAJTdVflWTkWQaH4gbT9iljKYCq1rJytQ8",
    "AIzaSyDWyPsDjoAg-XHDOx2PxuBaqSSHQ6JoGtg",
    "AIzaSyD48TmzBNR-lZjEoDJApPyc2G9nyuXpxIw",
    "AIzaSyDe7IHF5iCxegDTwEkBwFYBIGA1LleIjcQ",
    "AIzaSyCtm8n8IH6Gpk2aWqk9_WZGh50ihSsgYqg",
    "AIzaSyC0p7T-ygPCVZbgH9ZxhTBYHAkHfP696gE",
    "AIzaSyD6wmOoMxB0TKPRI8oJiMwHoVCCMozl-ck",
    "AIzaSyCdUzQiRtXHQaaX8OadXQIeR2tM5mSnZmo",
    "AIzaSyDloBpPfDzAdAX-MLqgd7nesdJbYLKlNc0",
    "AIzaSyBLDQs07EhkpBVyum6e1WZA0nRDlk9ctI0",
    "AIzaSyB9dQEda4hX3uBkV3Gxd3V3cLJeSWws4Gw",
    "AIzaSyA5ecNchFRDVrnFshUwCG_YCjtga6bmewo",
    "AIzaSyDGk2Fw9ro0Tkn6gsRyyMbLgTTqVLgEwCQ",
    "AIzaSyDcI870uDH15WNCrGpZGh6VBdquRx7qN_Y",
    "AIzaSyC3TXcXNe6RR6oaBBxYUKV0Au8VtkUrsRI",
    "AIzaSyBBDXBsCDEezZJ6hgBNUbUSLjXqOoSwXbo"
]

# API Configuration
API_CONFIG = {
    "base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
    "timeout": 30,
    "max_retries": 3,
    "cooldown_period": 600,  # 10 minutes in seconds
    "max_failures": 3
}

# Security Configuration
SECURITY_CONFIG = {
    "allowed_origins": ["http://localhost:8501"],  # Add your production domain here
    "rate_limit": {
        "requests_per_minute": 60,
        "burst_limit": 10
    }
} 