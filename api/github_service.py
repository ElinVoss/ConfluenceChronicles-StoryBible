"""
GitHub API Service for AI Model Integration

This module provides a comprehensive interface for AI models to interact with
the Confluence Chronicles Story Bible repository through GitHub's REST API.

Features:
- File operations (read, write, create, update)
- Branch management
- Pull request operations
- Issue management
- Commit operations
- Content search and retrieval
"""

import os
import base64
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests


class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors"""
    pass


class GitHubService:
    """
    Main service class for GitHub API operations.

    Supports both personal access tokens and GitHub App authentication.
    """

    def __init__(self, token: Optional[str] = None, owner: Optional[str] = None, repo: Optional[str] = None):
        """
        Initialize GitHub service.

        Args:
            token: GitHub personal access token or app token (defaults to GITHUB_TOKEN env var)
            owner: Repository owner (defaults to GITHUB_OWNER env var)
            repo: Repository name (defaults to GITHUB_REPO env var)
        """
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.owner = owner or os.environ.get('GITHUB_OWNER', 'ElinVoss')
        self.repo = repo or os.environ.get('GITHUB_REPO', 'ConfluenceChronicles-StoryBible')

        if not self.token:
            raise GitHubAPIError("GitHub token is required. Set GITHUB_TOKEN environment variable.")

        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Make authenticated request to GitHub API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint (without base URL)
            **kwargs: Additional arguments for requests

        Returns:
            Response JSON data

        Raises:
            GitHubAPIError: If request fails
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()

            # Some endpoints return 204 No Content
            if response.status_code == 204:
                return {"status": "success", "message": "Operation completed successfully"}

            return response.json()

        except requests.exceptions.HTTPError as e:
            error_msg = f"GitHub API error: {e.response.status_code} - {e.response.text}"
            raise GitHubAPIError(error_msg)
        except requests.exceptions.RequestException as e:
            raise GitHubAPIError(f"Request failed: {str(e)}")

    # ========================
    # File Operations
    # ========================

    def get_file(self, path: str, branch: str = "main") -> Dict[str, Any]:
        """
        Get file content from repository.

        Args:
            path: File path in repository
            branch: Branch name (default: main)

        Returns:
            Dictionary with file metadata and decoded content
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/contents/{path}"
        params = {"ref": branch}

        data = self._request("GET", endpoint, params=params)

        # Decode base64 content
        if data.get("content"):
            content = base64.b64decode(data["content"]).decode('utf-8')
            data["decoded_content"] = content

        return data

    def create_or_update_file(
        self,
        path: str,
        content: str,
        message: str,
        branch: str = "main",
        sha: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create or update a file in the repository.

        Args:
            path: File path in repository
            content: File content (will be base64 encoded)
            message: Commit message
            branch: Branch name
            sha: File SHA (required for updates, get from get_file())

        Returns:
            Commit information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/contents/{path}"

        # Encode content to base64
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

        payload = {
            "message": message,
            "content": encoded_content,
            "branch": branch
        }

        if sha:
            payload["sha"] = sha

        return self._request("PUT", endpoint, json=payload)

    def delete_file(
        self,
        path: str,
        message: str,
        sha: str,
        branch: str = "main"
    ) -> Dict[str, Any]:
        """
        Delete a file from the repository.

        Args:
            path: File path in repository
            message: Commit message
            sha: File SHA (required, get from get_file())
            branch: Branch name

        Returns:
            Commit information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/contents/{path}"

        payload = {
            "message": message,
            "sha": sha,
            "branch": branch
        }

        return self._request("DELETE", endpoint, json=payload)

    def get_directory_contents(self, path: str = "", branch: str = "main") -> List[Dict[str, Any]]:
        """
        Get contents of a directory.

        Args:
            path: Directory path (empty string for root)
            branch: Branch name

        Returns:
            List of file/directory metadata
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/contents/{path}"
        params = {"ref": branch}

        return self._request("GET", endpoint, params=params)

    # ========================
    # Branch Operations
    # ========================

    def list_branches(self) -> List[Dict[str, Any]]:
        """
        List all branches in the repository.

        Returns:
            List of branch information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/branches"
        return self._request("GET", endpoint)

    def get_branch(self, branch: str) -> Dict[str, Any]:
        """
        Get information about a specific branch.

        Args:
            branch: Branch name

        Returns:
            Branch information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/branches/{branch}"
        return self._request("GET", endpoint)

    def create_branch(self, branch: str, from_branch: str = "main") -> Dict[str, Any]:
        """
        Create a new branch from an existing branch.

        Args:
            branch: New branch name
            from_branch: Source branch name

        Returns:
            Reference information
        """
        # Get SHA of source branch
        source = self.get_branch(from_branch)
        sha = source["commit"]["sha"]

        # Create new branch reference
        endpoint = f"/repos/{self.owner}/{self.repo}/git/refs"
        payload = {
            "ref": f"refs/heads/{branch}",
            "sha": sha
        }

        return self._request("POST", endpoint, json=payload)

    # ========================
    # Pull Request Operations
    # ========================

    def create_pull_request(
        self,
        title: str,
        head: str,
        base: str = "main",
        body: Optional[str] = None,
        draft: bool = False
    ) -> Dict[str, Any]:
        """
        Create a pull request.

        Args:
            title: PR title
            head: Branch containing changes
            base: Base branch (target)
            body: PR description
            draft: Create as draft PR

        Returns:
            Pull request information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/pulls"

        payload = {
            "title": title,
            "head": head,
            "base": base,
            "draft": draft
        }

        if body:
            payload["body"] = body

        return self._request("POST", endpoint, json=payload)

    def list_pull_requests(
        self,
        state: str = "open",
        sort: str = "created",
        direction: str = "desc"
    ) -> List[Dict[str, Any]]:
        """
        List pull requests.

        Args:
            state: PR state (open, closed, all)
            sort: Sort by (created, updated, popularity, long-running)
            direction: Sort direction (asc, desc)

        Returns:
            List of pull requests
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/pulls"
        params = {
            "state": state,
            "sort": sort,
            "direction": direction
        }

        return self._request("GET", endpoint, params=params)

    def get_pull_request(self, pr_number: int) -> Dict[str, Any]:
        """
        Get details of a specific pull request.

        Args:
            pr_number: Pull request number

        Returns:
            Pull request information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/pulls/{pr_number}"
        return self._request("GET", endpoint)

    def update_pull_request(
        self,
        pr_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        base: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a pull request.

        Args:
            pr_number: Pull request number
            title: New title
            body: New body
            state: New state (open, closed)
            base: New base branch

        Returns:
            Updated pull request information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/pulls/{pr_number}"

        payload = {}
        if title:
            payload["title"] = title
        if body:
            payload["body"] = body
        if state:
            payload["state"] = state
        if base:
            payload["base"] = base

        return self._request("PATCH", endpoint, json=payload)

    def merge_pull_request(
        self,
        pr_number: int,
        commit_title: Optional[str] = None,
        commit_message: Optional[str] = None,
        merge_method: str = "merge"
    ) -> Dict[str, Any]:
        """
        Merge a pull request.

        Args:
            pr_number: Pull request number
            commit_title: Title for merge commit
            commit_message: Message for merge commit
            merge_method: Merge method (merge, squash, rebase)

        Returns:
            Merge information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/pulls/{pr_number}/merge"

        payload = {"merge_method": merge_method}
        if commit_title:
            payload["commit_title"] = commit_title
        if commit_message:
            payload["commit_message"] = commit_message

        return self._request("PUT", endpoint, json=payload)

    def add_pr_comment(self, pr_number: int, body: str) -> Dict[str, Any]:
        """
        Add a comment to a pull request.

        Args:
            pr_number: Pull request number
            body: Comment text

        Returns:
            Comment information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/issues/{pr_number}/comments"
        payload = {"body": body}

        return self._request("POST", endpoint, json=payload)

    # ========================
    # Issue Operations
    # ========================

    def create_issue(
        self,
        title: str,
        body: Optional[str] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create an issue.

        Args:
            title: Issue title
            body: Issue description
            labels: List of label names
            assignees: List of usernames to assign

        Returns:
            Issue information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/issues"

        payload = {"title": title}
        if body:
            payload["body"] = body
        if labels:
            payload["labels"] = labels
        if assignees:
            payload["assignees"] = assignees

        return self._request("POST", endpoint, json=payload)

    def list_issues(
        self,
        state: str = "open",
        labels: Optional[List[str]] = None,
        sort: str = "created",
        direction: str = "desc"
    ) -> List[Dict[str, Any]]:
        """
        List issues.

        Args:
            state: Issue state (open, closed, all)
            labels: Filter by labels
            sort: Sort by (created, updated, comments)
            direction: Sort direction (asc, desc)

        Returns:
            List of issues
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/issues"
        params = {
            "state": state,
            "sort": sort,
            "direction": direction
        }

        if labels:
            params["labels"] = ",".join(labels)

        return self._request("GET", endpoint, params=params)

    def get_issue(self, issue_number: int) -> Dict[str, Any]:
        """
        Get details of a specific issue.

        Args:
            issue_number: Issue number

        Returns:
            Issue information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/issues/{issue_number}"
        return self._request("GET", endpoint)

    def update_issue(
        self,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update an issue.

        Args:
            issue_number: Issue number
            title: New title
            body: New body
            state: New state (open, closed)
            labels: New labels

        Returns:
            Updated issue information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/issues/{issue_number}"

        payload = {}
        if title:
            payload["title"] = title
        if body:
            payload["body"] = body
        if state:
            payload["state"] = state
        if labels:
            payload["labels"] = labels

        return self._request("PATCH", endpoint, json=payload)

    def add_issue_comment(self, issue_number: int, body: str) -> Dict[str, Any]:
        """
        Add a comment to an issue.

        Args:
            issue_number: Issue number
            body: Comment text

        Returns:
            Comment information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/issues/{issue_number}/comments"
        payload = {"body": body}

        return self._request("POST", endpoint, json=payload)

    # ========================
    # Search Operations
    # ========================

    def search_code(self, query: str, max_results: int = 30) -> List[Dict[str, Any]]:
        """
        Search code in the repository.

        Args:
            query: Search query (automatically scoped to this repo)
            max_results: Maximum number of results

        Returns:
            List of code search results
        """
        endpoint = "/search/code"
        full_query = f"{query} repo:{self.owner}/{self.repo}"
        params = {
            "q": full_query,
            "per_page": min(max_results, 100)
        }

        result = self._request("GET", endpoint, params=params)
        return result.get("items", [])

    def search_issues(self, query: str, max_results: int = 30) -> List[Dict[str, Any]]:
        """
        Search issues and pull requests.

        Args:
            query: Search query (automatically scoped to this repo)
            max_results: Maximum number of results

        Returns:
            List of issue search results
        """
        endpoint = "/search/issues"
        full_query = f"{query} repo:{self.owner}/{self.repo}"
        params = {
            "q": full_query,
            "per_page": min(max_results, 100)
        }

        result = self._request("GET", endpoint, params=params)
        return result.get("items", [])

    # ========================
    # Commit Operations
    # ========================

    def list_commits(
        self,
        branch: Optional[str] = None,
        path: Optional[str] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        max_results: int = 30
    ) -> List[Dict[str, Any]]:
        """
        List commits in the repository.

        Args:
            branch: Filter by branch
            path: Filter by file path
            since: Only commits after this date (ISO 8601)
            until: Only commits before this date (ISO 8601)
            max_results: Maximum number of results

        Returns:
            List of commits
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/commits"
        params = {"per_page": min(max_results, 100)}

        if branch:
            params["sha"] = branch
        if path:
            params["path"] = path
        if since:
            params["since"] = since
        if until:
            params["until"] = until

        return self._request("GET", endpoint, params=params)

    def get_commit(self, sha: str) -> Dict[str, Any]:
        """
        Get details of a specific commit.

        Args:
            sha: Commit SHA

        Returns:
            Commit information
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/commits/{sha}"
        return self._request("GET", endpoint)

    # ========================
    # Repository Operations
    # ========================

    def get_repository_info(self) -> Dict[str, Any]:
        """
        Get repository information.

        Returns:
            Repository metadata
        """
        endpoint = f"/repos/{self.owner}/{self.repo}"
        return self._request("GET", endpoint)

    def get_readme(self, branch: str = "main") -> Dict[str, Any]:
        """
        Get repository README content.

        Args:
            branch: Branch name

        Returns:
            README metadata and content
        """
        endpoint = f"/repos/{self.owner}/{self.repo}/readme"
        params = {"ref": branch}

        data = self._request("GET", endpoint, params=params)

        # Decode base64 content
        if data.get("content"):
            content = base64.b64decode(data["content"]).decode('utf-8')
            data["decoded_content"] = content

        return data


# ========================
# Utility Functions
# ========================

def create_service(token: Optional[str] = None) -> GitHubService:
    """
    Factory function to create GitHubService instance.

    Args:
        token: Optional GitHub token (defaults to env var)

    Returns:
        Configured GitHubService instance
    """
    return GitHubService(token=token)


if __name__ == "__main__":
    # Example usage
    try:
        service = create_service()

        # Test connection
        repo_info = service.get_repository_info()
        print(f"✓ Connected to: {repo_info['full_name']}")
        print(f"  Description: {repo_info['description']}")
        print(f"  Default branch: {repo_info['default_branch']}")

        # List recent commits
        commits = service.list_commits(max_results=5)
        print(f"\n✓ Recent commits ({len(commits)}):")
        for commit in commits:
            message = commit['commit']['message'].split('\n')[0]
            print(f"  - {commit['sha'][:7]}: {message}")

    except GitHubAPIError as e:
        print(f"✗ Error: {e}")
