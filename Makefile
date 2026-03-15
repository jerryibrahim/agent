DEST := $(HOME)/.claude
SRC  := .claude

.PHONY: copy-claude-md copy-claude-settings copy-claude-skill copy-claude-skills copy-claude-all

## Copy CLAUDE.md and CLAUDE_lessons.md to ~/.claude
copy-claude-md:
	@mkdir -p $(DEST)
	cp $(SRC)/CLAUDE.md $(DEST)/CLAUDE.md
	cp $(SRC)/CLAUDE_lessons.md $(DEST)/CLAUDE_lessons.md
	@echo "Copied CLAUDE.md and CLAUDE_lessons.md to $(DEST)"

## Copy settings.json to ~/.claude
copy-claude-settings:
	@mkdir -p $(DEST)
	cp $(SRC)/settings.json $(DEST)/settings.json
	@echo "Copied settings.json to $(DEST)"

## Copy a specific skill: make copy-claude-skill SKILL=commit
copy-claude-skill:
ifndef SKILL
	$(error Usage: make copy-claude-skill SKILL=<skill-name>)
endif
	@mkdir -p $(DEST)/skills
	cp -r $(SRC)/skills/$(SKILL) $(DEST)/skills/$(SKILL)
	@echo "Copied skill '$(SKILL)' to $(DEST)/skills/$(SKILL)"

## Copy all skills to ~/.claude/skills
copy-claude-skills:
	@mkdir -p $(DEST)/skills
	cp -r $(SRC)/skills/* $(DEST)/skills/
	@echo "Copied all skills to $(DEST)/skills"

## Copy entire .claude folder to ~/.claude
copy-claude-all:
	@mkdir -p $(DEST)
	cp -r $(SRC)/* $(DEST)/
	@echo "Copied entire .claude folder to $(DEST)"
