compile:
	transcrypt -nab --xtrans="npx babel --presets=react --plugins=emotion" --parent=.none src/index.py

.PHONY: compile
