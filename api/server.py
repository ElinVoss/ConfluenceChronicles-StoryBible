"""
REST API Server for AI Bible API

This Flask-based server exposes the AI Bible API via HTTP endpoints,
allowing AI models to interact with the repository through standard REST calls.

Usage:
    python api/server.py

Environment variables:
    GITHUB_TOKEN: Required GitHub personal access token
    API_PORT: Port to run server on (default: 5000)
    API_HOST: Host to bind to (default: 0.0.0.0)
"""

import os
import json
from typing import Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps

from .ai_bible_api import AIBibleAPI, create_ai_api
from .github_service import GitHubAPIError


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize API
try:
    bible_api = create_ai_api()
except Exception as e:
    print(f"Warning: Could not initialize API at startup: {e}")
    print("Make sure GITHUB_TOKEN is set in environment variables")
    bible_api = None


# ========================
# Error Handlers
# ========================

def handle_errors(f):
    """Decorator to handle API errors consistently"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except GitHubAPIError as e:
            return jsonify({
                "error": "GitHub API Error",
                "message": str(e)
            }), 400
        except ValueError as e:
            return jsonify({
                "error": "Validation Error",
                "message": str(e)
            }), 400
        except Exception as e:
            return jsonify({
                "error": "Internal Server Error",
                "message": str(e)
            }), 500
    return decorated_function


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "The requested endpoint does not exist"
    }), 404


# ========================
# Health & Status Endpoints
# ========================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "api_version": "1.0.0",
        "service": "AI Bible API"
    })


@app.route('/status', methods=['GET'])
@handle_errors
def get_status():
    """Get repository status"""
    status = bible_api.get_status()
    return jsonify(status)


# ========================
# Canon Endpoints
# ========================

@app.route('/canon/lexicon', methods=['GET'])
@handle_errors
def get_lexicon():
    """Get master lexicon"""
    branch = request.args.get('branch')
    lexicon = bible_api.get_master_lexicon(branch)
    return jsonify(lexicon)


@app.route('/canon/soulpulse', methods=['GET'])
@handle_errors
def get_soulpulse():
    """Get Soulpulse Resonance system documentation"""
    branch = request.args.get('branch')
    soulpulse = bible_api.get_soulpulse_system(branch)
    return jsonify(soulpulse)


@app.route('/canon/knowledge-gates', methods=['GET'])
@handle_errors
def get_knowledge_gates():
    """Get knowledge gate rules"""
    era = request.args.get('era')
    branch = request.args.get('branch')
    gates = bible_api.get_knowledge_gates(era, branch)
    return jsonify(gates)


@app.route('/canon/files', methods=['GET'])
@handle_errors
def list_canon_files():
    """List all canon files"""
    branch = request.args.get('branch')
    files = bible_api.list_canon_files(branch)
    return jsonify({"files": files})


# ========================
# Novella Endpoints
# ========================

@app.route('/novellas', methods=['GET'])
@handle_errors
def list_novellas():
    """List all novellas"""
    branch = request.args.get('branch')
    novellas = bible_api.list_novellas(branch)
    return jsonify({"novellas": novellas})


@app.route('/novellas/<novella_id>/brief', methods=['GET'])
@handle_errors
def get_novella_brief(novella_id: str):
    """Get novella brief"""
    branch = request.args.get('branch')
    brief = bible_api.get_novella_brief(novella_id, branch)
    return jsonify(brief)


@app.route('/novellas/<novella_id>/brief', methods=['POST'])
@handle_errors
def create_novella_brief(novella_id: str):
    """Create novella brief"""
    data = request.get_json()

    if not data or 'brief_data' not in data:
        return jsonify({
            "error": "Missing required field",
            "message": "Request must include 'brief_data' field"
        }), 400

    brief_data = data['brief_data']
    branch = data.get('branch')
    commit_message = data.get('commit_message')

    result = bible_api.create_novella_brief(
        novella_id=novella_id,
        brief_data=brief_data,
        branch=branch,
        commit_message=commit_message
    )

    return jsonify(result), 201


@app.route('/novellas/<novella_id>/generate-bible', methods=['POST'])
@handle_errors
def generate_story_bible(novella_id: str):
    """Generate story bible workflow"""
    data = request.get_json() or {}

    brief_data = data.get('brief_data')
    create_pr = data.get('create_pr', True)
    base_branch = data.get('base_branch')

    result = bible_api.generate_story_bible_workflow(
        novella_id=novella_id,
        brief_data=brief_data,
        create_pr=create_pr,
        base_branch=base_branch
    )

    return jsonify(result), 201


# ========================
# Character Endpoints
# ========================

@app.route('/characters', methods=['GET'])
@handle_errors
def list_characters():
    """List all characters"""
    branch = request.args.get('branch')
    characters = bible_api.list_characters(branch)
    return jsonify({"characters": characters})


@app.route('/characters/<character_name>', methods=['GET'])
@handle_errors
def get_character(character_name: str):
    """Get character file"""
    branch = request.args.get('branch')
    character = bible_api.get_character_file(character_name, branch)
    return jsonify(character)


# ========================
# Search Endpoints
# ========================

@app.route('/search/canon', methods=['GET'])
@handle_errors
def search_canon():
    """Search canonical documentation"""
    query = request.args.get('q')
    max_results = int(request.args.get('max_results', 20))

    if not query:
        return jsonify({
            "error": "Missing parameter",
            "message": "Query parameter 'q' is required"
        }), 400

    results = bible_api.search_canon(query, max_results)
    return jsonify({"results": results, "count": len(results)})


@app.route('/search/novellas', methods=['GET'])
@handle_errors
def search_novellas():
    """Search novella documentation"""
    query = request.args.get('q')
    max_results = int(request.args.get('max_results', 20))

    if not query:
        return jsonify({
            "error": "Missing parameter",
            "message": "Query parameter 'q' is required"
        }), 400

    results = bible_api.search_novellas(query, max_results)
    return jsonify({"results": results, "count": len(results)})


@app.route('/search', methods=['GET'])
@handle_errors
def search_all():
    """Search entire repository"""
    query = request.args.get('q')
    max_results = int(request.args.get('max_results', 30))

    if not query:
        return jsonify({
            "error": "Missing parameter",
            "message": "Query parameter 'q' is required"
        }), 400

    results = bible_api.search_all(query, max_results)
    return jsonify({"results": results, "count": len(results)})


# ========================
# File Operations Endpoints
# ========================

@app.route('/files', methods=['GET'])
@handle_errors
def get_file():
    """Get file content"""
    path = request.args.get('path')
    branch = request.args.get('branch', 'main')

    if not path:
        return jsonify({
            "error": "Missing parameter",
            "message": "Query parameter 'path' is required"
        }), 400

    file_data = bible_api.github.get_file(path, branch)
    return jsonify({
        "path": path,
        "content": file_data.get("decoded_content"),
        "sha": file_data["sha"],
        "size": file_data["size"]
    })


@app.route('/files', methods=['POST', 'PUT'])
@handle_errors
def create_or_update_file():
    """Create or update file"""
    data = request.get_json()

    required_fields = ['path', 'content', 'message']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": "Missing required field",
                "message": f"Request must include '{field}' field"
            }), 400

    result = bible_api.github.create_or_update_file(
        path=data['path'],
        content=data['content'],
        message=data['message'],
        branch=data.get('branch', 'main'),
        sha=data.get('sha')
    )

    return jsonify(result), 201


# ========================
# Pull Request Endpoints
# ========================

@app.route('/pulls', methods=['GET'])
@handle_errors
def list_pull_requests():
    """List pull requests"""
    state = request.args.get('state', 'open')
    prs = bible_api.github.list_pull_requests(state=state)
    return jsonify({"pull_requests": prs, "count": len(prs)})


@app.route('/pulls', methods=['POST'])
@handle_errors
def create_pull_request():
    """Create pull request"""
    data = request.get_json()

    required_fields = ['title', 'head']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": "Missing required field",
                "message": f"Request must include '{field}' field"
            }), 400

    pr = bible_api.github.create_pull_request(
        title=data['title'],
        head=data['head'],
        base=data.get('base', 'main'),
        body=data.get('body'),
        draft=data.get('draft', False)
    )

    return jsonify(pr), 201


@app.route('/pulls/<int:pr_number>', methods=['GET'])
@handle_errors
def get_pull_request(pr_number: int):
    """Get pull request details"""
    pr = bible_api.github.get_pull_request(pr_number)
    return jsonify(pr)


@app.route('/pulls/<int:pr_number>/comments', methods=['POST'])
@handle_errors
def add_pr_comment(pr_number: int):
    """Add comment to pull request"""
    data = request.get_json()

    if not data or 'body' not in data:
        return jsonify({
            "error": "Missing required field",
            "message": "Request must include 'body' field"
        }), 400

    comment = bible_api.github.add_pr_comment(pr_number, data['body'])
    return jsonify(comment), 201


# ========================
# Issue Endpoints
# ========================

@app.route('/issues', methods=['GET'])
@handle_errors
def list_issues():
    """List issues"""
    state = request.args.get('state', 'open')
    labels = request.args.getlist('labels')

    issues = bible_api.github.list_issues(
        state=state,
        labels=labels if labels else None
    )

    return jsonify({"issues": issues, "count": len(issues)})


@app.route('/issues', methods=['POST'])
@handle_errors
def create_issue():
    """Create issue"""
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({
            "error": "Missing required field",
            "message": "Request must include 'title' field"
        }), 400

    issue = bible_api.github.create_issue(
        title=data['title'],
        body=data.get('body'),
        labels=data.get('labels'),
        assignees=data.get('assignees')
    )

    return jsonify(issue), 201


@app.route('/issues/<int:issue_number>', methods=['GET'])
@handle_errors
def get_issue(issue_number: int):
    """Get issue details"""
    issue = bible_api.github.get_issue(issue_number)
    return jsonify(issue)


@app.route('/issues/<int:issue_number>/comments', methods=['POST'])
@handle_errors
def add_issue_comment(issue_number: int):
    """Add comment to issue"""
    data = request.get_json()

    if not data or 'body' not in data:
        return jsonify({
            "error": "Missing required field",
            "message": "Request must include 'body' field"
        }), 400

    comment = bible_api.github.add_issue_comment(issue_number, data['body'])
    return jsonify(comment), 201


# ========================
# Workflow Endpoints
# ========================

@app.route('/workflows/content-pr', methods=['POST'])
@handle_errors
def create_content_pr():
    """Create PR with multiple file changes"""
    data = request.get_json()

    required_fields = ['title', 'files']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": "Missing required field",
                "message": f"Request must include '{field}' field"
            }), 400

    result = bible_api.create_content_pr(
        title=data['title'],
        files=data['files'],
        description=data.get('description'),
        base_branch=data.get('base_branch'),
        labels=data.get('labels')
    )

    return jsonify(result), 201


# ========================
# Main
# ========================

if __name__ == '__main__':
    # Get configuration from environment
    host = os.environ.get('API_HOST', '0.0.0.0')
    port = int(os.environ.get('API_PORT', 5000))
    debug = os.environ.get('API_DEBUG', 'false').lower() == 'true'

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              AI Bible API Server                             ║
║              Confluence Chronicles Story Bible               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Server Configuration:
  Host: {host}
  Port: {port}
  Debug: {debug}

Environment:
  GITHUB_TOKEN: {'✓ Set' if os.environ.get('GITHUB_TOKEN') else '✗ Not set'}
  GITHUB_OWNER: {os.environ.get('GITHUB_OWNER', 'ElinVoss')}
  GITHUB_REPO: {os.environ.get('GITHUB_REPO', 'ConfluenceChronicles-StoryBible')}

Available Endpoints:
  GET  /health                      - Health check
  GET  /status                      - Repository status
  GET  /canon/lexicon               - Get master lexicon
  GET  /canon/soulpulse              - Get magic system docs
  GET  /novellas                    - List all novellas
  POST /novellas/:id/generate-bible - Generate story bible
  GET  /search?q=...                - Search repository
  POST /pulls                       - Create pull request
  POST /issues                      - Create issue

For full API documentation, see: api/README.md

Starting server...
""")

    app.run(host=host, port=port, debug=debug)
