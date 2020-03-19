#!/bin/bash

cd $(dirname $0)

if [ -f .make.local.sh ]; then
	source .make.local.sh
else
	echo "Missing .make.local.sh"
fi

if [ "$2" = "" ]; then
	./.venv/bin/python put_and_dump.py $FILENAMES_FOR_BACKUP
else
	./.venv/bin/python put_and_dump.py $FILENAMES_FOR_BACKUP --key $1 --value $2
fi
