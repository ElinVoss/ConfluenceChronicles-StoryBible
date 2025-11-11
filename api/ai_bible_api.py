"""
AI Bible API - High-level interface for AI models to interact with Story Bible

This module provides AI-friendly operations specifically designed for the
Confluence Chronicles Story Bible workflow, including:
- Canon retrieval and validation
- Novella brief management
- Story bible generation
- Automated PR workflows
- Lexicon and knowledge gate validation
"""

import os
import json
import yaml
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from .github_service import GitHubService, GitHubAPIError


class AIBibleAPI:
    """
    High-level API for AI models to interact with the Story Bible repository.

    This class wraps the GitHub service with story bible-specific operations.
    """

    def __init__(self, github_service: Optional[GitHubService] = None):
        """
        Initialize AI Bible API.

        Args:
            github_service: Optional GitHubService instance (creates new if not provided)
        """
        self.github = github_service or GitHubService()
        self.default_branch = "main"

    # ========================
    # Canon Operations
    # ========================

    def get_master_lexicon(self, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the master lexicon (canonical terminology).

        Args:
            branch: Branch name (defaults to main)

        Returns:
            Dictionary with lexicon content and metadata
        """
        branch = branch or self.default_branch
        file_data = self.github.get_file("docs/01-canon/master-lexicon.md", branch)

        return {
            "content": file_data["decoded_content"],
            "sha": file_data["sha"],
            "path": file_data["path"],
            "size": file_data["size"]
        }

    def get_soulpulse_system(self, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the Soulpulse Resonance magic system documentation.

        Args:
            branch: Branch name (defaults to main)

        Returns:
            Dictionary with magic system content and metadata
        """
        branch = branch or self.default_branch
        file_data = self.github.get_file(
            "docs/01-canon/soulpulse-resonance-system-production-canon.md",
            branch
        )

        return {
            "content": file_data["decoded_content"],
            "sha": file_data["sha"],
            "path": file_data["path"],
            "size": file_data["size"]
        }

    def get_knowledge_gates(self, era: Optional[str] = None, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Get knowledge gate rules (progressive reveal system).

        Args:
            era: Specific era (e.g., "N01", "N05") - returns all if not specified
            branch: Branch name (defaults to main)

        Returns:
            Dictionary with knowledge gate content and metadata
        """
        branch = branch or self.default_branch

        # Get the main knowledge gates file
        file_data = self.github.get_file(
            "docs/01-canon/knowledge-gates-and-scene-ladder-N01-N05.md",
            branch
        )

        result = {
            "content": file_data["decoded_content"],
            "sha": file_data["sha"],
            "path": file_data["path"]
        }

        # If specific era requested, also get era-specific scope
        if era:
            try:
                era_file = self.github.get_file(
                    f"docs/01-canon/{era}-Soulpulse-Scope.md",
                    branch
                )
                result["era_specific"] = {
                    "content": era_file["decoded_content"],
                    "sha": era_file["sha"],
                    "era": era
                }
            except GitHubAPIError:
                result["era_specific"] = None

        return result

    def list_canon_files(self, branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all canonical files in the repository.

        Args:
            branch: Branch name (defaults to main)

        Returns:
            List of canon file metadata
        """
        branch = branch or self.default_branch
        return self.github.get_directory_contents("docs/01-canon", branch)

    # ========================
    # Novella Operations
    # ========================

    def get_novella_brief(self, novella_id: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a novella brief (YAML configuration).

        Args:
            novella_id: Novella identifier (e.g., "N01")
            branch: Branch name (defaults to main)

        Returns:
            Dictionary with parsed YAML brief and metadata
        """
        branch = branch or self.default_branch

        # Try multiple possible locations
        possible_paths = [
            f"docs/05-ops/novella-briefs/{novella_id}-brief.yaml",
            f"docs/04-plot/novellas/{novella_id}/{novella_id}-brief.yaml",
            f"briefs/{novella_id}-brief.yaml"
        ]

        for path in possible_paths:
            try:
                file_data = self.github.get_file(path, branch)
                brief_data = yaml.safe_load(file_data["decoded_content"])

                return {
                    "novella_id": novella_id,
                    "brief": brief_data,
                    "raw_content": file_data["decoded_content"],
                    "sha": file_data["sha"],
                    "path": path
                }
            except GitHubAPIError:
                continue

        raise GitHubAPIError(f"Novella brief not found for {novella_id}")

    def create_novella_brief(
        self,
        novella_id: str,
        brief_data: Dict[str, Any],
        branch: Optional[str] = None,
        commit_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new novella brief.

        Args:
            novella_id: Novella identifier (e.g., "N06")
            brief_data: Brief data dictionary
            branch: Branch name (defaults to main)
            commit_message: Custom commit message

        Returns:
            Creation confirmation with file metadata
        """
        branch = branch or self.default_branch
        path = f"docs/05-ops/novella-briefs/{novella_id}-brief.yaml"

        # Convert to YAML
        yaml_content = yaml.dump(brief_data, sort_keys=False, allow_unicode=True)

        message = commit_message or f"feat: add novella brief for {novella_id}"

        result = self.github.create_or_update_file(
            path=path,
            content=yaml_content,
            message=message,
            branch=branch
        )

        return {
            "novella_id": novella_id,
            "path": path,
            "commit": result["commit"],
            "status": "created"
        }

    def list_novellas(self, branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all novella directories.

        Args:
            branch: Branch name (defaults to main)

        Returns:
            List of novella metadata
        """
        branch = branch or self.default_branch
        contents = self.github.get_directory_contents("docs/04-plot/novellas", branch)

        # Filter for directories that look like novella IDs
        novellas = []
        for item in contents:
            if item["type"] == "dir" and item["name"].startswith("N"):
                novellas.append({
                    "novella_id": item["name"],
                    "path": item["path"],
                    "url": item["html_url"]
                })

        return sorted(novellas, key=lambda x: x["novella_id"])

    # ========================
    # Story Bible Generation
    # ========================

    def generate_story_bible_workflow(
        self,
        novella_id: str,
        brief_data: Optional[Dict[str, Any]] = None,
        create_pr: bool = True,
        base_branch: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Full workflow to generate a story bible:
        1. Create a feature branch
        2. Create/update novella brief if provided
        3. Generate instructions for running forge_bible.py
        4. Optionally create a PR

        Args:
            novella_id: Novella identifier
            brief_data: Optional brief data (uses existing if not provided)
            create_pr: Whether to create a pull request
            base_branch: Base branch for PR (defaults to main)

        Returns:
            Dictionary with workflow results
        """
        base_branch = base_branch or self.default_branch
        feature_branch = f"ai/generate-bible-{novella_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        workflow_result = {
            "novella_id": novella_id,
            "feature_branch": feature_branch,
            "steps": []
        }

        # Step 1: Create feature branch
        try:
            branch_result = self.github.create_branch(feature_branch, base_branch)
            workflow_result["steps"].append({
                "step": "create_branch",
                "status": "success",
                "branch": feature_branch
            })
        except GitHubAPIError as e:
            workflow_result["steps"].append({
                "step": "create_branch",
                "status": "failed",
                "error": str(e)
            })
            return workflow_result

        # Step 2: Create/update brief if provided
        if brief_data:
            try:
                brief_result = self.create_novella_brief(
                    novella_id=novella_id,
                    brief_data=brief_data,
                    branch=feature_branch
                )
                workflow_result["steps"].append({
                    "step": "create_brief",
                    "status": "success",
                    "path": brief_result["path"]
                })
            except GitHubAPIError as e:
                workflow_result["steps"].append({
                    "step": "create_brief",
                    "status": "failed",
                    "error": str(e)
                })

        # Step 3: Add instructions for running forge_bible.py
        workflow_result["instructions"] = {
            "message": "To generate the story bible, run the following command locally:",
            "command": f"python tools/forge_bible.py --brief docs/05-ops/novella-briefs/{novella_id}-brief.yaml --output products/{novella_id}-story-bible",
            "note": "The forge_bible.py script requires OpenAI API access and cannot be run directly via GitHub API"
        }

        # Step 4: Create PR if requested
        if create_pr:
            try:
                pr_title = f"Generate story bible for {novella_id}"
                pr_body = f"""## Story Bible Generation Workflow

This PR sets up the workflow for generating the story bible for **{novella_id}**.

### What's included:
- Novella brief configuration

### Next steps:
To generate the actual story bible content, run:
```bash
python tools/forge_bible.py --brief docs/05-ops/novella-briefs/{novella_id}-brief.yaml --output products/{novella_id}-story-bible
```

### AI Bible Engine
This follows the AI Bible Engine contract defined in `docs/05-ops/ai-bible-engine.md`.

---
*Generated by AI Bible API*
"""

                pr_result = self.github.create_pull_request(
                    title=pr_title,
                    head=feature_branch,
                    base=base_branch,
                    body=pr_body,
                    draft=True
                )

                workflow_result["steps"].append({
                    "step": "create_pr",
                    "status": "success",
                    "pr_number": pr_result["number"],
                    "pr_url": pr_result["html_url"]
                })
                workflow_result["pr_url"] = pr_result["html_url"]

            except GitHubAPIError as e:
                workflow_result["steps"].append({
                    "step": "create_pr",
                    "status": "failed",
                    "error": str(e)
                })

        return workflow_result

    # ========================
    # Validation Operations
    # ========================

    def validate_lexicon(
        self,
        content: str,
        novella_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate content against master lexicon rules.

        Note: This requires the lexicon_lint.py tool to be available.

        Args:
            content: Content to validate
            novella_id: Optional novella ID for context

        Returns:
            Validation results
        """
        # This would typically call the lexicon_lint.py script
        # For now, return structure for what validation would look like
        return {
            "status": "validation_available_via_cli",
            "message": "Run: python tools/lint/lexicon_lint.py <file_path>",
            "novella_id": novella_id,
            "note": "Lexicon validation requires running the Python linter locally or via CI"
        }

    def validate_knowledge_gates(
        self,
        content: str,
        novella_id: str
    ) -> Dict[str, Any]:
        """
        Validate content against knowledge gate rules for specific era.

        Args:
            content: Content to validate
            novella_id: Novella ID (determines era)

        Returns:
            Validation results
        """
        return {
            "status": "validation_available_via_cli",
            "message": f"Run: python tools/lint/knowledge_gate_lint.py --era {novella_id} <file_path>",
            "novella_id": novella_id,
            "note": "Knowledge gate validation requires running the Python linter locally or via CI"
        }

    # ========================
    # Character & Plot Operations
    # ========================

    def get_character_file(self, character_name: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a character definition file.

        Args:
            character_name: Character name (filename without extension)
            branch: Branch name (defaults to main)

        Returns:
            Character file content and metadata
        """
        branch = branch or self.default_branch
        path = f"docs/03-characters/{character_name}.md"

        file_data = self.github.get_file(path, branch)

        return {
            "character": character_name,
            "content": file_data["decoded_content"],
            "sha": file_data["sha"],
            "path": path
        }

    def list_characters(self, branch: Optional[str] = None) -> List[str]:
        """
        List all character files.

        Args:
            branch: Branch name (defaults to main)

        Returns:
            List of character names
        """
        branch = branch or self.default_branch
        contents = self.github.get_directory_contents("docs/03-characters", branch)

        characters = []
        for item in contents:
            if item["type"] == "file" and item["name"].endswith(".md"):
                character_name = item["name"].replace(".md", "")
                characters.append(character_name)

        return sorted(characters)

    # ========================
    # Search & Discovery
    # ========================

    def search_canon(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Search within canonical documentation.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of search results
        """
        full_query = f"{query} path:docs/01-canon"
        return self.github.search_code(full_query, max_results)

    def search_novellas(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Search within novella documentation.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of search results
        """
        full_query = f"{query} path:docs/04-plot/novellas"
        return self.github.search_code(full_query, max_results)

    def search_all(self, query: str, max_results: int = 30) -> List[Dict[str, Any]]:
        """
        Search entire repository.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of search results
        """
        return self.github.search_code(query, max_results)

    # ========================
    # Workflow Operations
    # ========================

    def create_content_pr(
        self,
        title: str,
        files: Dict[str, str],
        description: Optional[str] = None,
        base_branch: Optional[str] = None,
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a PR with multiple file changes.

        Args:
            title: PR title
            files: Dictionary of {file_path: content}
            description: PR description
            base_branch: Base branch (defaults to main)
            labels: Labels to add to PR

        Returns:
            PR information
        """
        base_branch = base_branch or self.default_branch
        feature_branch = f"ai/content-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        # Create feature branch
        self.github.create_branch(feature_branch, base_branch)

        # Commit all files
        for file_path, content in files.items():
            commit_message = f"Add/update {file_path}"
            self.github.create_or_update_file(
                path=file_path,
                content=content,
                message=commit_message,
                branch=feature_branch
            )

        # Create PR
        pr_body = description or "Automated content update via AI Bible API"
        pr_result = self.github.create_pull_request(
            title=title,
            head=feature_branch,
            base=base_branch,
            body=pr_body,
            draft=False
        )

        return {
            "pr_number": pr_result["number"],
            "pr_url": pr_result["html_url"],
            "feature_branch": feature_branch,
            "files_updated": list(files.keys())
        }

    # ========================
    # Repository Status
    # ========================

    def get_status(self) -> Dict[str, Any]:
        """
        Get overall repository status and statistics.

        Returns:
            Repository status information
        """
        repo_info = self.github.get_repository_info()
        branches = self.github.list_branches()
        recent_commits = self.github.list_commits(max_results=5)

        return {
            "repository": {
                "name": repo_info["full_name"],
                "description": repo_info.get("description"),
                "default_branch": repo_info["default_branch"],
                "updated_at": repo_info["updated_at"]
            },
            "branches": {
                "total": len(branches),
                "names": [b["name"] for b in branches[:10]]
            },
            "recent_activity": {
                "latest_commit": {
                    "sha": recent_commits[0]["sha"][:7],
                    "message": recent_commits[0]["commit"]["message"].split("\n")[0],
                    "author": recent_commits[0]["commit"]["author"]["name"],
                    "date": recent_commits[0]["commit"]["author"]["date"]
                }
            }
        }


# ========================
# Factory Function
# ========================

def create_ai_api(token: Optional[str] = None) -> AIBibleAPI:
    """
    Factory function to create AIBibleAPI instance.

    Args:
        token: Optional GitHub token (defaults to env var)

    Returns:
        Configured AIBibleAPI instance
    """
    github_service = GitHubService(token=token)
    return AIBibleAPI(github_service)


if __name__ == "__main__":
    # Example usage
    try:
        api = create_ai_api()

        # Get status
        status = api.get_status()
        print(f"✓ Repository: {status['repository']['name']}")
        print(f"  Description: {status['repository']['description']}")

        # List novellas
        novellas = api.list_novellas()
        print(f"\n✓ Found {len(novellas)} novellas:")
        for novella in novellas[:5]:
            print(f"  - {novella['novella_id']}")

        # Get master lexicon
        lexicon = api.get_master_lexicon()
        print(f"\n✓ Master Lexicon: {len(lexicon['content'])} characters")

    except GitHubAPIError as e:
        print(f"✗ Error: {e}")
