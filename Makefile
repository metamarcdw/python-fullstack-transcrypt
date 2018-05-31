compile:
	transcrypt -nab --xtrans="npx babel --presets=react" --parent=.none src/index.py

.PHONY: compile
