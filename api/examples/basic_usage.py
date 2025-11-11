#!/usr/bin/env python3
"""
Basic usage examples for AI Bible API

This script demonstrates the fundamental operations available through
the AI Bible API.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import create_ai_api, GitHubAPIError


def main():
    print("=" * 70)
    print("AI Bible API - Basic Usage Examples")
    print("=" * 70)

    try:
        # Initialize API
        print("\n1. Initializing API...")
        api = create_ai_api()
        print("   ✓ API initialized successfully")

        # Get repository status
        print("\n2. Getting repository status...")
        status = api.get_status()
        print(f"   ✓ Repository: {status['repository']['name']}")
        print(f"   ✓ Description: {status['repository']['description']}")
        print(f"   ✓ Default branch: {status['repository']['default_branch']}")
        print(f"   ✓ Branches: {status['branches']['total']}")

        # Get master lexicon
        print("\n3. Getting master lexicon...")
        lexicon = api.get_master_lexicon()
        print(f"   ✓ Lexicon size: {len(lexicon['content'])} characters")
        print(f"   ✓ Path: {lexicon['path']}")
        print(f"   ✓ First 200 chars: {lexicon['content'][:200]}...")

        # Get Soulpulse system
        print("\n4. Getting Soulpulse Resonance system...")
        soulpulse = api.get_soulpulse_system()
        print(f"   ✓ Document size: {len(soulpulse['content'])} characters")
        print(f"   ✓ Path: {soulpulse['path']}")

        # Get knowledge gates
        print("\n5. Getting knowledge gates for N01...")
        gates = api.get_knowledge_gates(era="N01")
        print(f"   ✓ Knowledge gates retrieved")
        print(f"   ✓ Path: {gates['path']}")
        if gates.get('era_specific'):
            print(f"   ✓ Era-specific file: {gates['era_specific']['era']}")

        # List novellas
        print("\n6. Listing novellas...")
        novellas = api.list_novellas()
        print(f"   ✓ Found {len(novellas)} novellas:")
        for novella in novellas[:5]:
            print(f"      - {novella['novella_id']}")
        if len(novellas) > 5:
            print(f"      ... and {len(novellas) - 5} more")

        # List characters
        print("\n7. Listing characters...")
        characters = api.list_characters()
        if characters:
            print(f"   ✓ Found {len(characters)} characters:")
            for character in characters[:5]:
                print(f"      - {character}")
            if len(characters) > 5:
                print(f"      ... and {len(characters) - 5} more")
        else:
            print("   ℹ No character files found yet")

        # Search canon
        print("\n8. Searching canon for 'Soulpulse'...")
        results = api.search_canon("Soulpulse", max_results=5)
        print(f"   ✓ Found {len(results)} results")
        for i, result in enumerate(results[:3], 1):
            print(f"      {i}. {result['path']}")

        # List canon files
        print("\n9. Listing canon files...")
        canon_files = api.list_canon_files()
        print(f"   ✓ Found {len(canon_files)} canon files:")
        for file in canon_files[:5]:
            print(f"      - {file['name']} ({file['size']} bytes)")

        print("\n" + "=" * 70)
        print("All basic operations completed successfully!")
        print("=" * 70)

    except GitHubAPIError as e:
        print(f"\n✗ GitHub API Error: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
