#!/bin/bash
if [ ! -d .venv ]; then
	virtualenv -p `which python3` .venv
fi

./.venv/bin/pip install -r requirements.txt

# CERTFI_PATH=`./.venv/bin/python -c 'import certifi; print(certifi.where())'`
# rm $CERTFI_PATH
# ln -sf /etc/ssl/certs/ca-certificates.crt $CERTFI_PATH
