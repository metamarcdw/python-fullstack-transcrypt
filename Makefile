compile:
	transcrypt -nab --xtrans="node_modules/.bin/babel --presets=react --plugins=emotion" --parent=.none src/index.py

.PHONY: compile
