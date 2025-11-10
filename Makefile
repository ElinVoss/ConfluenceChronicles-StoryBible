lint:
	python tools/lint/lexicon_lint.py docs || true
	python tools/lint/knowledge_gate_lint.py --era N01 docs || true
