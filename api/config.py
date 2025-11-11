"""
Configuration management for AI Bible API

Loads configuration from environment variables and provides defaults.
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration class for AI Bible API"""

    def __init__(self):
        """Initialize configuration from environment variables"""

        # Load .env file if it exists
        self._load_dotenv()

        # GitHub Configuration
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.github_owner = os.environ.get('GITHUB_OWNER', 'ElinVoss')
        self.github_repo = os.environ.get('GITHUB_REPO', 'ConfluenceChronicles-StoryBible')

        # OpenAI Configuration
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')

        # API Server Configuration
        self.api_host = os.environ.get('API_HOST', '0.0.0.0')
        self.api_port = int(os.environ.get('API_PORT', 5000))
        self.api_debug = os.environ.get('API_DEBUG', 'false').lower() == 'true'

        # Repository Configuration
        self.default_branch = os.environ.get('DEFAULT_BRANCH', 'main')

    def _load_dotenv(self):
        """Load environment variables from .env file if it exists"""
        env_path = Path(__file__).parent / '.env'

        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = line.split('=', 1)
                            # Only set if not already in environment
                            if key not in os.environ:
                                os.environ[key] = value
                        except ValueError:
                            continue

    def validate(self) -> bool:
        """
        Validate required configuration.

        Returns:
            True if configuration is valid, False otherwise
        """
        required_vars = {
            'GITHUB_TOKEN': self.github_token
        }

        missing = [key for key, value in required_vars.items() if not value]

        if missing:
            print(f"Missing required configuration: {', '.join(missing)}")
            return False

        return True

    def __repr__(self) -> str:
        """String representation of configuration (masks secrets)"""
        return f"""Config(
    github_owner={self.github_owner},
    github_repo={self.github_repo},
    github_token={'***' if self.github_token else 'Not set'},
    openai_api_key={'***' if self.openai_api_key else 'Not set'},
    api_host={self.api_host},
    api_port={self.api_port},
    api_debug={self.api_debug},
    default_branch={self.default_branch}
)"""


# Global config instance
config = Config()


if __name__ == '__main__':
    # Test configuration
    print("Current Configuration:")
    print(config)
    print(f"\nValid: {config.validate()}")
