#!/bin/bash
cd web
su -m app -c "flask run --host 0.0.0.0"
