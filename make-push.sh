#!/bin/bash

cd $(dirname $0)

if [ -f .make.local.sh ]; then
	source .make.local.sh
else
	echo "Missing .make.local.sh"
fi

./.venv/bin/python push_kv.py $FILENAMES_TO_PUSH
read
./.venv/bin/python push_kv.py $FILENAMES_TO_PUSH --update
