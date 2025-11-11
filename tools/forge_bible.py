#!/usr/bin/env python3
"""
Confluence Chronicles - AI Story-Bible Forge Script

This script automates the generation of novella-specific story bibles by:
1. Reading a novella brief (YAML)
2. Loading relevant canon files
3. Calling an LLM with the AI Bible Engine system prompt
4. Parsing the output into the proper file structure
5. Writing files to products/<novella-id>-story-bible/

REQUIREMENTS:
- Python 3.10+
- openai package: pip3 install openai
- Environment variable: OPENAI_API_KEY

USAGE:
    python tools/forge_bible.py --novella-brief docs/05-ops/N01-brief.yaml
    python tools/forge_bible.py --novella-brief docs/05-ops/N01-brief.yaml --output-dir custom/path
    python tools/forge_bible.py --novella-brief docs/05-ops/N01-brief.yaml --model gpt-4.1-mini
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip3 install pyyaml")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: OpenAI package not installed. Run: pip3 install openai")
    sys.exit(1)


class BibleForge:
    """Orchestrates the generation of novella-specific story bibles."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.client = None
        
    def initialize_llm_client(self, model: str = "gpt-4.1-mini") -> None:
        """Initialize OpenAI client using environment variables."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable not set. "
                "Please set it with your OpenAI API key."
            )
        
        # Client initialization uses env vars automatically
        self.client = OpenAI()
        self.model = model
        print(f"✓ Initialized LLM client (model: {model})")
    
    def load_system_prompt(self) -> str:
        """Load the AI Bible Engine system prompt."""
        prompt_path = self.repo_root / "prompts" / "ai-bible-engine-system.txt"
        if not prompt_path.exists():
            raise FileNotFoundError(f"System prompt not found: {prompt_path}")
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"✓ Loaded system prompt ({len(content)} chars)")
        return content
    
    def load_novella_brief(self, brief_path: Path) -> Dict:
        """Load and parse the novella brief YAML."""
        if not brief_path.exists():
            raise FileNotFoundError(f"Novella brief not found: {brief_path}")
        
        with open(brief_path, "r", encoding="utf-8") as f:
            brief = yaml.safe_load(f)
        
        # Validate required fields
        required_fields = ["novella_id", "working_title", "era", "target_length_words"]
        missing = [f for f in required_fields if f not in brief]
        if missing:
            raise ValueError(f"Brief missing required fields: {missing}")
        
        print(f"✓ Loaded brief for {brief['novella_id']}: {brief['working_title']}")
        return brief
    
    def load_canon_context(self, novella_era: str) -> str:
        """Load relevant canon files to provide context to the LLM."""
        canon_dir = self.repo_root / "docs" / "01-canon"
        
        # Always include master lexicon
        lexicon_path = canon_dir / "master-lexicon.md"
        knowledge_gates_path = canon_dir / "knowledge-gates-and-scene-ladder-N01-N05.md"
        magic_system_path = canon_dir / "soulpulse-resonance-system-production-canon.md"
        
        canon_parts = []
        
        # Load master lexicon (first 200 lines for context)
        if lexicon_path.exists():
            with open(lexicon_path, "r", encoding="utf-8") as f:
                lines = f.readlines()[:200]
                canon_parts.append(f"## MASTER LEXICON (excerpt)\n\n{''.join(lines)}")
        
        # Load knowledge gates
        if knowledge_gates_path.exists():
            with open(knowledge_gates_path, "r", encoding="utf-8") as f:
                canon_parts.append(f"## KNOWLEDGE GATES\n\n{f.read()}")
        
        # Load magic system (first 150 lines)
        if magic_system_path.exists():
            with open(magic_system_path, "r", encoding="utf-8") as f:
                lines = f.readlines()[:150]
                canon_parts.append(f"## SOULPULSE SYSTEM (excerpt)\n\n{''.join(lines)}")
        
        canon_context = "\n\n---\n\n".join(canon_parts)
        print(f"✓ Loaded canon context ({len(canon_context)} chars)")
        return canon_context
    
    def build_user_message(self, brief: Dict, canon_context: str) -> str:
        """Construct the user message with canon context and brief."""
        brief_yaml = yaml.dump(brief, default_flow_style=False, sort_keys=False)
        
        message = f"""# CANON CONTEXT

{canon_context}

---

# NOVELLA BRIEF

```yaml
{brief_yaml}
```

---

# TASK

Generate a complete novella-specific story bible for the above brief, following the structure and rules defined in your system prompt.

Output each file as a markdown section with the file path as the heading, like this:

## 00-brief/novella-brief.yaml

```yaml
[content]
```

## 01-canon-overrides/canon-deltas.md

[content]

Continue for all required files. Be specific and concrete; no placeholders or "TBD" content.
"""
        return message
    
    def call_llm(self, system_prompt: str, user_message: str) -> str:
        """Call the LLM to generate the story bible."""
        print(f"→ Calling LLM (model: {self.model})...")
        print(f"  System prompt: {len(system_prompt)} chars")
        print(f"  User message: {len(user_message)} chars")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=16000  # Adjust based on model limits
            )
            
            content = response.choices[0].message.content
            print(f"✓ Received response ({len(content)} chars)")
            return content
            
        except Exception as e:
            raise RuntimeError(f"LLM call failed: {e}")
    
    def parse_output(self, llm_output: str) -> Dict[str, str]:
        """Parse LLM output into a dict of {filepath: content}."""
        files = {}
        
        # Match markdown sections like: ## path/to/file.ext
        pattern = r'^##\s+(.+?)$'
        sections = re.split(pattern, llm_output, flags=re.MULTILINE)
        
        # sections[0] is preamble (ignore), then alternating [path, content, path, content...]
        for i in range(1, len(sections), 2):
            if i + 1 >= len(sections):
                break
            
            filepath = sections[i].strip()
            content = sections[i + 1].strip()
            
            # Clean up YAML fences if present
            if filepath.endswith('.yaml') or filepath.endswith('.yml'):
                content = re.sub(r'^```ya?ml\s*\n', '', content, flags=re.MULTILINE)
                content = re.sub(r'\n```\s*$', '', content, flags=re.MULTILINE)
            
            # Clean up markdown fences if present
            content = re.sub(r'^```markdown\s*\n', '', content, flags=re.MULTILINE)
            content = re.sub(r'\n```\s*$', '', content, flags=re.MULTILINE)
            
            files[filepath] = content.strip()
        
        print(f"✓ Parsed {len(files)} files from output")
        return files
    
    def write_files(self, files: Dict[str, str], output_dir: Path) -> List[Path]:
        """Write parsed files to the output directory."""
        output_dir.mkdir(parents=True, exist_ok=True)
        written_files = []
        
        for filepath, content in files.items():
            full_path = output_dir / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
                if not content.endswith('\n'):
                    f.write('\n')  # POSIX compliance
            
            written_files.append(full_path)
            print(f"  ✓ {filepath}")
        
        return written_files
    
    def generate_bible(
        self,
        brief_path: Path,
        output_dir: Optional[Path] = None,
        model: str = "gpt-4.1-mini"
    ) -> Path:
        """Main orchestration method."""
        print("\n" + "="*60)
        print("CONFLUENCE CHRONICLES - AI STORY-BIBLE FORGE")
        print("="*60 + "\n")
        
        # Initialize
        self.initialize_llm_client(model)
        
        # Load inputs
        system_prompt = self.load_system_prompt()
        brief = self.load_novella_brief(brief_path)
        canon_context = self.load_canon_context(brief.get("era", "Turning_1"))
        
        # Determine output directory
        if output_dir is None:
            novella_id = brief["novella_id"]
            output_dir = self.repo_root / "products" / f"{novella_id}-story-bible"
        
        print(f"→ Output directory: {output_dir}")
        
        # Build message and call LLM
        user_message = self.build_user_message(brief, canon_context)
        llm_output = self.call_llm(system_prompt, user_message)
        
        # Parse and write files
        files = self.parse_output(llm_output)
        if not files:
            raise RuntimeError("No files parsed from LLM output. Check output format.")
        
        print(f"\n→ Writing {len(files)} files to {output_dir}...")
        written_files = self.write_files(files, output_dir)
        
        print(f"\n✓ Successfully generated story bible at: {output_dir}")
        print(f"  Total files: {len(written_files)}")
        
        return output_dir


def main():
    parser = argparse.ArgumentParser(
        description="Generate novella-specific story bibles for Confluence Chronicles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/forge_bible.py --novella-brief docs/05-ops/N01-brief.yaml
  python tools/forge_bible.py --novella-brief docs/05-ops/N17-brief.yaml --model gpt-4.1-mini
  python tools/forge_bible.py --novella-brief docs/05-ops/N01-brief.yaml --output-dir custom/path

Environment Variables:
  OPENAI_API_KEY    Required. Your OpenAI API key.
        """
    )
    
    parser.add_argument(
        "--novella-brief",
        type=Path,
        required=True,
        help="Path to the novella brief YAML file (e.g., docs/05-ops/N01-brief.yaml)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: products/<novella-id>-story-bible/)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4.1-mini",
        help="LLM model to use (default: gpt-4.1-mini)"
    )
    
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root directory (default: auto-detect)"
    )
    
    args = parser.parse_args()
    
    # Determine repo root
    if args.repo_root:
        repo_root = args.repo_root
    else:
        # Assume script is in tools/ subdirectory
        repo_root = Path(__file__).parent.parent
    
    if not repo_root.exists():
        print(f"ERROR: Repository root not found: {repo_root}")
        sys.exit(1)
    
    # Run the forge
    try:
        forge = BibleForge(repo_root)
        output_dir = forge.generate_bible(
            brief_path=args.novella_brief,
            output_dir=args.output_dir,
            model=args.model
        )
        
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print(f"1. Review the generated bible at: {output_dir}")
        print(f"2. Run linters: make lint")
        print(f"3. Check canon compliance and character arc specificity")
        print(f"4. Iterate if needed, then commit to repository")
        print()
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
