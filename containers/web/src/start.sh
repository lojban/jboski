#!/bin/bash

gunicorn jboski:app --access-logfile - --error-logfile - --access-logformat '%(h)s %({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' -w 1 -b 0.0.0.0:8080 
