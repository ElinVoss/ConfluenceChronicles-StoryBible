#!/usr/bin/env python3
"""
Example: REST API Client

This script demonstrates how to interact with the AI Bible API
through HTTP REST endpoints, which is how external AI models
would typically access the repository.
"""

import requests
import json
from typing import Dict, Any


class AIBibleClient:
    """Simple client for the AI Bible REST API"""

    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    # Health & Status
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        return self._request("GET", "/health")

    def get_status(self) -> Dict[str, Any]:
        """Get repository status"""
        return self._request("GET", "/status")

    # Canon
    def get_lexicon(self) -> Dict[str, Any]:
        """Get master lexicon"""
        return self._request("GET", "/canon/lexicon")

    def get_soulpulse(self) -> Dict[str, Any]:
        """Get Soulpulse system"""
        return self._request("GET", "/canon/soulpulse")

    def get_knowledge_gates(self, era: str = None) -> Dict[str, Any]:
        """Get knowledge gates"""
        params = {"era": era} if era else {}
        return self._request("GET", "/canon/knowledge-gates", params=params)

    # Novellas
    def list_novellas(self) -> Dict[str, Any]:
        """List all novellas"""
        return self._request("GET", "/novellas")

    def get_novella_brief(self, novella_id: str) -> Dict[str, Any]:
        """Get novella brief"""
        return self._request("GET", f"/novellas/{novella_id}/brief")

    def create_novella_brief(self, novella_id: str, brief_data: Dict) -> Dict[str, Any]:
        """Create novella brief"""
        payload = {"brief_data": brief_data}
        return self._request("POST", f"/novellas/{novella_id}/brief", json=payload)

    def generate_story_bible(
        self,
        novella_id: str,
        brief_data: Dict = None,
        create_pr: bool = True
    ) -> Dict[str, Any]:
        """Generate story bible workflow"""
        payload = {
            "brief_data": brief_data,
            "create_pr": create_pr
        }
        return self._request("POST", f"/novellas/{novella_id}/generate-bible", json=payload)

    # Search
    def search(self, query: str, scope: str = "all", max_results: int = 30) -> Dict[str, Any]:
        """
        Search repository

        Args:
            query: Search query
            scope: 'all', 'canon', or 'novellas'
            max_results: Max number of results
        """
        endpoint = f"/search/{scope}" if scope != "all" else "/search"
        params = {"q": query, "max_results": max_results}
        return self._request("GET", endpoint, params=params)

    # Pull Requests
    def create_pull_request(
        self,
        title: str,
        head: str,
        base: str = "main",
        body: str = None
    ) -> Dict[str, Any]:
        """Create pull request"""
        payload = {
            "title": title,
            "head": head,
            "base": base,
            "body": body
        }
        return self._request("POST", "/pulls", json=payload)

    def list_pull_requests(self, state: str = "open") -> Dict[str, Any]:
        """List pull requests"""
        params = {"state": state}
        return self._request("GET", "/pulls", params=params)


def main():
    print("=" * 70)
    print("AI Bible API - REST Client Example")
    print("=" * 70)

    # Initialize client
    print("\nMake sure the API server is running:")
    print("  python api/server.py")
    print("\nThen run this script in another terminal.\n")

    input("Press Enter when server is ready...")

    client = AIBibleClient()

    try:
        # Health check
        print("\n1. Health Check...")
        health = client.health_check()
        print(f"   ✓ Status: {health['status']}")
        print(f"   ✓ Version: {health['api_version']}")

        # Get status
        print("\n2. Repository Status...")
        status = client.get_status()
        print(f"   ✓ Repository: {status['repository']['name']}")
        print(f"   ✓ Branches: {status['branches']['total']}")

        # Get lexicon
        print("\n3. Get Master Lexicon...")
        lexicon = client.get_lexicon()
        print(f"   ✓ Size: {len(lexicon['content'])} characters")
        print(f"   ✓ Path: {lexicon['path']}")

        # Get knowledge gates
        print("\n4. Get Knowledge Gates (N01)...")
        gates = client.get_knowledge_gates(era="N01")
        print(f"   ✓ Retrieved knowledge gates")
        print(f"   ✓ Path: {gates['path']}")

        # List novellas
        print("\n5. List Novellas...")
        novellas = client.list_novellas()
        print(f"   ✓ Found {len(novellas['novellas'])} novellas")
        for novella in novellas['novellas'][:3]:
            print(f"      - {novella['novella_id']}")

        # Search
        print("\n6. Search Canon for 'Soulpulse'...")
        results = client.search("Soulpulse", scope="canon", max_results=5)
        print(f"   ✓ Found {results['count']} results")
        for result in results['results'][:3]:
            print(f"      - {result['path']}")

        # List PRs
        print("\n7. List Open Pull Requests...")
        prs = client.list_pull_requests(state="open")
        print(f"   ✓ Found {len(prs['pull_requests'])} open PRs")

        print("\n" + "=" * 70)
        print("All REST API operations completed successfully!")
        print("=" * 70)

        # Example: Generate story bible (commented out)
        print("\n" + "=" * 70)
        print("Example: Generate Story Bible (commented out)")
        print("=" * 70)
        print("""
# To generate a story bible via REST API:

brief_data = {
    "novella_id": "N10",
    "working_title": "Example Novella",
    "era": "middle",
    "target_length_words": 80000
}

result = client.generate_story_bible(
    novella_id="N10",
    brief_data=brief_data,
    create_pr=True
)

print(f"PR created: {result['pr_url']}")
""")

    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to API server")
        print("   Make sure the server is running:")
        print("   python api/server.py")
        return 1
    except requests.exceptions.HTTPError as e:
        print(f"\n✗ HTTP Error: {e}")
        print(f"   Response: {e.response.text}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
