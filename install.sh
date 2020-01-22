#!/bin/bash
if [ ! -d .venv ]; then
	virtualenv -p `which python3` .venv
fi

./.venv/bin/pip install -r requirements.txt
