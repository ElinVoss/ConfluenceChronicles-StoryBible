#!/usr/bin/env python3
"""
Example: Creating content and pull requests

This script demonstrates how to:
1. Create a feature branch
2. Add/update files
3. Create a pull request
4. Add comments to PRs
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import create_ai_api, GitHubAPIError


def main():
    print("=" * 70)
    print("AI Bible API - Content Creation Example")
    print("=" * 70)

    try:
        # Initialize API
        print("\n1. Initializing API...")
        api = create_ai_api()
        print("   ✓ API initialized")

        # Example: Create a multi-file PR
        print("\n2. Creating a multi-file PR example...")
        print("   This demonstrates how an AI model can create content")

        # Define the content to add
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Example character file
        character_content = """# Rynn Ashforge

## Overview
A young apprentice in the Glass Quarter with an untapped affinity for heat manipulation.

## Background
- Age: 19 casting
- Origin: Glass Quarter, lower districts
- Occupation: Forge apprentice

## Soulpulse Affinity
- Primary: Heat affinity (latent, not yet awakened in N01-N03)
- Manifestation: Will emerge in N04
- Costs: TBD based on first manifestation

## Character Arc
### N01-N03 (Early Era)
- Appears as background character
- Shows signs of heat sensitivity
- No knowledge of Soulpulse

### N04-N06 (Awakening)
- First manifestation during crisis
- Begins to understand costs
- Seeks guidance

## Relationships
- Mentor: Master Thornwright (forge-master)
- Ally: Kael (fellow seeker)

## Notes
- Designed to show "ordinary person" perspective
- Will be POV character in N05
- Critical to underground network subplot

## Canon Compliance
- Uses only approved lexicon terms
- Respects knowledge gates (no early-era leakage)
- Costs will be physiological (vein-burn patterns)
"""

        # Example plot note
        plot_note = """# Plot Note: Underground Network Reveal

## Timing
N05, Chapter 18

## Beat
Rynn discovers that the "accidents" in forges are actually:
- Manifestations of latent Soulpulse affinities
- Being suppressed by authorities
- Part of larger pattern across districts

## Setup Required
- N01-N04: Scattered mentions of forge accidents
- N04: Rynn's first manifestation (personal)
- N05: Pattern recognition

## Payoff
- Leads to underground network discovery
- Sets up N06-N08 arc
- Reveals systemic suppression

## Characters Involved
- Rynn (POV, discovery)
- Kael (investigation partner)
- Master Thornwright (knowing accomplice)

## Constraints
- No "resonance" terminology yet
- Focus on physical/practical costs
- Keep mystery elements strong
"""

        # Files to create
        files_to_create = {
            f"docs/03-characters/rynn-ashforge.md": character_content,
            f"docs/04-plot/novellas/N05/plot-notes/underground-network-reveal.md": plot_note
        }

        print(f"   Files to create:")
        for path in files_to_create.keys():
            print(f"      - {path}")

        # Confirm before proceeding
        print("\n   ⚠ This will create an actual PR in the repository!")
        print("   ⚠ Comment out the next section to just see the example without creating PR")

        # COMMENT OUT THE NEXT BLOCK TO AVOID CREATING ACTUAL PR
        """
        response = input("\n   Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("   Cancelled by user")
            return 0

        # Create the PR
        print("\n3. Creating pull request...")
        result = api.create_content_pr(
            title=f"AI Example: Add Rynn Ashforge character and plot notes",
            files=files_to_create,
            description=f'''## AI-Generated Content Example

This PR was created by the AI Bible API as a demonstration of automated content creation.

### What's included:
- Character file: Rynn Ashforge
- Plot note: Underground network reveal (N05)

### Canon compliance:
- Uses approved lexicon terminology
- Respects knowledge gate rules
- Includes cost tracking for Soulpulse manifestation

### Note
This is an example PR created at {datetime.now().isoformat()} to demonstrate API capabilities.

---
*Created by AI Bible API Example Script*
''',
            labels=["ai-generated", "example"]
        )

        print(f"   ✓ PR created successfully!")
        print(f"   ✓ PR number: {result['pr_number']}")
        print(f"   ✓ PR URL: {result['pr_url']}")
        print(f"   ✓ Feature branch: {result['feature_branch']}")
        print(f"   ✓ Files updated: {len(result['files_updated'])}")

        # Add a comment to the PR
        print("\n4. Adding comment to PR...")
        comment_body = '''## AI Review

I've created this content following these guidelines:

✓ **Lexicon Compliance**: Uses only approved terms from master lexicon
✓ **Knowledge Gates**: Respects N01-N05 limitations (no resonance terminology)
✓ **Cost Tracking**: Includes physiological costs (vein-burn)
✓ **Canon Integration**: Connects to existing plot threads

### Recommendations:
1. Review character arc timing
2. Verify plot note alignment with N05 outline
3. Confirm underground network subplot fits turning structure

### Next Steps:
- Run lexicon linter: `python tools/lint/lexicon_lint.py docs/03-characters/rynn-ashforge.md`
- Run knowledge gate linter: `python tools/lint/knowledge_gate_lint.py --era N05 docs/04-plot/novellas/N05/`

Please review and provide feedback!
'''

        api.github.add_pr_comment(result['pr_number'], comment_body)
        print(f"   ✓ Comment added to PR")

        print("\n" + "=" * 70)
        print("Content creation example completed!")
        print(f"View your PR at: {result['pr_url']}")
        print("=" * 70)
        """

        print("\n   (PR creation code commented out - see script source)")
        print("\n" + "=" * 70)
        print("Example completed (no PR created in demo mode)")
        print("To actually create PR, uncomment the code block in the script")
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
