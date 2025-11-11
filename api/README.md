# AI Bible API

A comprehensive GitHub API integration for the Confluence Chronicles Story Bible, enabling AI models to directly interact with the repository.

## Overview

This API provides three levels of access:

1. **GitHubService** - Low-level GitHub API wrapper
2. **AIBibleAPI** - High-level story bible operations
3. **REST API Server** - HTTP endpoints for remote access

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Python API Usage](#python-api-usage)
- [REST API Usage](#rest-api-usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Error Handling](#error-handling)

## Installation

### Requirements

- Python 3.8+
- GitHub Personal Access Token with `repo` scope
- (Optional) OpenAI API key for story bible generation

### Install Dependencies

```bash
cd api
pip install -r requirements.txt
```

### Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:
```env
GITHUB_TOKEN=your_github_token_here
OPENAI_API_KEY=your_openai_key_here  # Optional
```

3. Create a GitHub token:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (full control of private repositories)
   - Copy the token to your `.env` file

## Quick Start

### Python API

```python
from api import create_ai_api

# Initialize API
api = create_ai_api()

# Get repository status
status = api.get_status()
print(f"Repository: {status['repository']['name']}")

# Get master lexicon
lexicon = api.get_master_lexicon()
print(f"Lexicon size: {len(lexicon['content'])} characters")

# List novellas
novellas = api.list_novellas()
for novella in novellas:
    print(f"- {novella['novella_id']}")
```

### REST API Server

```bash
# Start the server
python api/server.py

# Or use environment variables
API_PORT=8000 python api/server.py
```

Then access endpoints:

```bash
# Health check
curl http://localhost:5000/health

# Get repository status
curl http://localhost:5000/status

# Get master lexicon
curl http://localhost:5000/canon/lexicon

# List novellas
curl http://localhost:5000/novellas
```

## Authentication

All API calls require a GitHub Personal Access Token.

### Setting up authentication:

**Option 1: Environment variable**
```bash
export GITHUB_TOKEN="your_token_here"
```

**Option 2: .env file**
```env
GITHUB_TOKEN=your_token_here
```

**Option 3: Direct initialization**
```python
from api import GitHubService

service = GitHubService(token="your_token_here")
```

## Python API Usage

### GitHubService (Low-level)

Direct GitHub API operations:

```python
from api import create_service

github = create_service()

# Get file
file_data = github.get_file("docs/01-canon/master-lexicon.md")
content = file_data["decoded_content"]

# Create branch
github.create_branch("feature/new-content", from_branch="main")

# Create file
github.create_or_update_file(
    path="docs/new-file.md",
    content="# New Content",
    message="Add new file",
    branch="feature/new-content"
)

# Create pull request
pr = github.create_pull_request(
    title="Add new content",
    head="feature/new-content",
    base="main",
    body="This PR adds new content to the story bible"
)
```

### AIBibleAPI (High-level)

Story bible-specific operations:

```python
from api import create_ai_api

api = create_ai_api()

# Canon operations
lexicon = api.get_master_lexicon()
soulpulse = api.get_soulpulse_system()
gates = api.get_knowledge_gates(era="N01")

# Novella operations
novellas = api.list_novellas()
brief = api.get_novella_brief("N01")

# Create novella brief
brief_data = {
    "novella_id": "N06",
    "working_title": "The Forge Awakens",
    "era": "early",
    "target_length_words": 80000,
    "tone_pillars": ["tense", "grounded", "mysterious"],
    "themes": ["discovery", "cost of power"],
    "required_characters": ["Kael", "Mira"],
    "forbidden_elements": ["resonance terminology"],
    "must_hit_beats": ["First vein-burn", "Forge discovery"]
}

result = api.create_novella_brief("N06", brief_data)

# Generate story bible workflow
workflow = api.generate_story_bible_workflow(
    novella_id="N06",
    brief_data=brief_data,
    create_pr=True
)
print(f"PR created: {workflow['pr_url']}")

# Search operations
canon_results = api.search_canon("Soulpulse")
novella_results = api.search_novellas("Kael")

# Character operations
characters = api.list_characters()
kael = api.get_character_file("kael")
```

## REST API Usage

### Endpoints Overview

#### Health & Status
- `GET /health` - Health check
- `GET /status` - Repository status

#### Canon
- `GET /canon/lexicon` - Get master lexicon
- `GET /canon/soulpulse` - Get Soulpulse system
- `GET /canon/knowledge-gates` - Get knowledge gates
- `GET /canon/files` - List all canon files

#### Novellas
- `GET /novellas` - List all novellas
- `GET /novellas/:id/brief` - Get novella brief
- `POST /novellas/:id/brief` - Create novella brief
- `POST /novellas/:id/generate-bible` - Generate story bible

#### Characters
- `GET /characters` - List all characters
- `GET /characters/:name` - Get character file

#### Search
- `GET /search?q=query` - Search entire repository
- `GET /search/canon?q=query` - Search canon only
- `GET /search/novellas?q=query` - Search novellas only

#### Files
- `GET /files?path=...` - Get file content
- `POST /files` - Create or update file

#### Pull Requests
- `GET /pulls` - List pull requests
- `POST /pulls` - Create pull request
- `GET /pulls/:number` - Get PR details
- `POST /pulls/:number/comments` - Add PR comment

#### Issues
- `GET /issues` - List issues
- `POST /issues` - Create issue
- `GET /issues/:number` - Get issue details
- `POST /issues/:number/comments` - Add issue comment

#### Workflows
- `POST /workflows/content-pr` - Create PR with multiple files

### REST API Examples

#### Get Master Lexicon

```bash
curl http://localhost:5000/canon/lexicon
```

Response:
```json
{
  "content": "# Master Lexicon\n\n...",
  "sha": "abc123...",
  "path": "docs/01-canon/master-lexicon.md",
  "size": 54321
}
```

#### Create Novella Brief

```bash
curl -X POST http://localhost:5000/novellas/N06/brief \
  -H "Content-Type: application/json" \
  -d '{
    "brief_data": {
      "novella_id": "N06",
      "working_title": "The Forge Awakens",
      "era": "early",
      "target_length_words": 80000
    }
  }'
```

#### Generate Story Bible Workflow

```bash
curl -X POST http://localhost:5000/novellas/N06/generate-bible \
  -H "Content-Type: application/json" \
  -d '{
    "brief_data": {
      "novella_id": "N06",
      "working_title": "The Forge Awakens"
    },
    "create_pr": true
  }'
```

Response:
```json
{
  "novella_id": "N06",
  "feature_branch": "ai/generate-bible-N06-20250111-143022",
  "steps": [
    {"step": "create_branch", "status": "success"},
    {"step": "create_brief", "status": "success"},
    {"step": "create_pr", "status": "success", "pr_number": 5}
  ],
  "pr_url": "https://github.com/ElinVoss/ConfluenceChronicles-StoryBible/pull/5"
}
```

#### Search Canon

```bash
curl "http://localhost:5000/search/canon?q=Soulpulse&max_results=10"
```

#### Create Pull Request

```bash
curl -X POST http://localhost:5000/pulls \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Add new character: Elara",
    "head": "feature/add-elara",
    "base": "main",
    "body": "This PR adds the character file for Elara"
  }'
```

#### Create Issue

```bash
curl -X POST http://localhost:5000/issues \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Update knowledge gates for N10",
    "body": "Need to review and update knowledge gate rules for N10",
    "labels": ["enhancement", "canon"]
  }'
```

## API Reference

### GitHubService Methods

#### File Operations
- `get_file(path, branch="main")` - Get file content
- `create_or_update_file(path, content, message, branch, sha=None)` - Create/update file
- `delete_file(path, message, sha, branch)` - Delete file
- `get_directory_contents(path="", branch="main")` - List directory contents

#### Branch Operations
- `list_branches()` - List all branches
- `get_branch(branch)` - Get branch info
- `create_branch(branch, from_branch="main")` - Create new branch

#### Pull Request Operations
- `create_pull_request(title, head, base, body, draft)` - Create PR
- `list_pull_requests(state, sort, direction)` - List PRs
- `get_pull_request(pr_number)` - Get PR details
- `update_pull_request(pr_number, ...)` - Update PR
- `merge_pull_request(pr_number, ...)` - Merge PR
- `add_pr_comment(pr_number, body)` - Add comment

#### Issue Operations
- `create_issue(title, body, labels, assignees)` - Create issue
- `list_issues(state, labels, sort, direction)` - List issues
- `get_issue(issue_number)` - Get issue details
- `update_issue(issue_number, ...)` - Update issue
- `add_issue_comment(issue_number, body)` - Add comment

#### Search Operations
- `search_code(query, max_results)` - Search code
- `search_issues(query, max_results)` - Search issues

### AIBibleAPI Methods

#### Canon Operations
- `get_master_lexicon(branch)` - Get master lexicon
- `get_soulpulse_system(branch)` - Get magic system docs
- `get_knowledge_gates(era, branch)` - Get knowledge gates
- `list_canon_files(branch)` - List canon files

#### Novella Operations
- `get_novella_brief(novella_id, branch)` - Get brief
- `create_novella_brief(novella_id, brief_data, branch, commit_message)` - Create brief
- `list_novellas(branch)` - List all novellas
- `generate_story_bible_workflow(novella_id, brief_data, create_pr, base_branch)` - Full workflow

#### Character Operations
- `get_character_file(character_name, branch)` - Get character file
- `list_characters(branch)` - List all characters

#### Search Operations
- `search_canon(query, max_results)` - Search canon
- `search_novellas(query, max_results)` - Search novellas
- `search_all(query, max_results)` - Search everything

#### Workflow Operations
- `create_content_pr(title, files, description, base_branch, labels)` - Create multi-file PR
- `get_status()` - Get repository status

## Examples

### Example 1: Read Canon and Create Character

```python
from api import create_ai_api

api = create_ai_api()

# Read the master lexicon to understand terminology
lexicon = api.get_master_lexicon()
print("Understanding approved terminology...")

# Read the magic system
soulpulse = api.get_soulpulse_system()
print("Understanding Soulpulse Resonance system...")

# Create a new character file
character_content = """# Elara Thornsmith

## Overview
A skilled forge-master from the Glass Quarter...

## Soulpulse Affinity
- Primary: Heat affinity (early manifestation)
- Costs: Severe vein-burn along forearms...
"""

# Create PR with the character file
result = api.create_content_pr(
    title="Add character: Elara Thornsmith",
    files={
        "docs/03-characters/elara-thornsmith.md": character_content
    },
    description="New character for N06-N08 arc",
    labels=["character", "N06"]
)

print(f"PR created: {result['pr_url']}")
```

### Example 2: Generate Story Bible for New Novella

```python
from api import create_ai_api

api = create_ai_api()

# Define novella brief
brief_data = {
    "novella_id": "N07",
    "working_title": "Echoes of the Forge",
    "era": "early",
    "target_length_words": 85000,
    "tone_pillars": ["tense", "introspective", "mysterious"],
    "themes": [
        "cost of ambition",
        "hidden history",
        "trust and betrayal"
    ],
    "required_characters": ["Kael", "Elara", "Mira"],
    "forbidden_elements": [
        "resonance terminology",
        "god-vessels",
        "Confluence mechanics",
        "Hollowing"
    ],
    "must_hit_beats": [
        "Kael discovers forge records",
        "Elara's first major vein-burn",
        "Underground network revealed",
        "Betrayal at the Glass Quarter"
    ],
    "target_reading_level": "adult",
    "pov_style": "third-person limited (rotating)",
    "chapter_count": 24
}

# Run full workflow
workflow = api.generate_story_bible_workflow(
    novella_id="N07",
    brief_data=brief_data,
    create_pr=True
)

print(f"Workflow completed!")
print(f"Feature branch: {workflow['feature_branch']}")
print(f"PR URL: {workflow['pr_url']}")
print(f"\nNext step: {workflow['instructions']['command']}")
```

### Example 3: Search and Validate Content

```python
from api import create_ai_api

api = create_ai_api()

# Search for all mentions of a character
results = api.search_all("Kael")
print(f"Found {len(results)} mentions of Kael")

# Search for specific magic system terms
canon_results = api.search_canon("vein-burn")
print(f"Found {len(canon_results)} canon references to vein-burn")

# Get knowledge gates for a specific era
gates = api.get_knowledge_gates(era="N03")
print("Knowledge gate rules for N03:")
print(gates['content'][:500])
```

### Example 4: REST API from AI Model

```python
import requests

BASE_URL = "http://localhost:5000"

# Get repository status
response = requests.get(f"{BASE_URL}/status")
status = response.json()
print(f"Repository: {status['repository']['name']}")

# Search for content
response = requests.get(f"{BASE_URL}/search/canon", params={"q": "Soulpulse"})
results = response.json()
print(f"Found {results['count']} results")

# Create novella brief
brief = {
    "brief_data": {
        "novella_id": "N08",
        "working_title": "Shadows in Glass",
        "era": "early"
    }
}
response = requests.post(f"{BASE_URL}/novellas/N08/brief", json=brief)
print(f"Brief created: {response.json()}")

# Generate story bible
workflow = {
    "brief_data": brief["brief_data"],
    "create_pr": True
}
response = requests.post(f"{BASE_URL}/novellas/N08/generate-bible", json=workflow)
result = response.json()
print(f"PR created: {result['pr_url']}")
```

## Error Handling

All errors return consistent JSON responses:

```json
{
  "error": "Error Type",
  "message": "Detailed error message"
}
```

### Python API

```python
from api import create_ai_api, GitHubAPIError

api = create_ai_api()

try:
    file_data = api.github.get_file("nonexistent-file.md")
except GitHubAPIError as e:
    print(f"GitHub API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### REST API

```bash
curl http://localhost:5000/nonexistent-endpoint
```

Response (404):
```json
{
  "error": "Not Found",
  "message": "The requested endpoint does not exist"
}
```

## Security Considerations

1. **Never commit `.env` file** - It contains sensitive tokens
2. **Use environment variables** - Don't hardcode tokens in code
3. **Limit token scope** - Only grant necessary permissions
4. **Rotate tokens regularly** - Replace tokens periodically
5. **Use HTTPS in production** - Never send tokens over HTTP
6. **Validate input** - Always validate user input before API calls

## Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests
pytest api/

# With coverage
pytest --cov=api api/
```

### Code Formatting

```bash
# Install formatter
pip install black

# Format code
black api/
```

## Troubleshooting

### "GitHub token is required"
- Set `GITHUB_TOKEN` environment variable
- Or create `.env` file with `GITHUB_TOKEN=your_token`

### "404 Not Found" errors
- Check file paths are correct
- Verify branch exists
- Ensure token has `repo` scope

### "Rate limit exceeded"
- GitHub API has rate limits (5000 requests/hour for authenticated requests)
- Wait for limit reset or use conditional requests

### Server won't start
- Check port 5000 is not in use: `lsof -i :5000`
- Try different port: `API_PORT=8000 python api/server.py`

## License

All rights reserved. See main repository LICENSE file.

## Support

For issues or questions:
- GitHub Issues: https://github.com/ElinVoss/ConfluenceChronicles-StoryBible/issues
- Check existing documentation in `docs/05-ops/`

## Version History

### v1.0.0 (2025-11-11)
- Initial release
- GitHub API integration
- AI Bible API layer
- REST API server
- Full story bible workflow support
