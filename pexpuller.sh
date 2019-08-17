#! /bin/bash    
cd /home/admin/pexpuller
source venv/bin/activate
export USER="admin"
export PASSWORD="password"
export MGR_ADDRESS="mgr.customer.com"
# virtualenv is now active, which means your PATH has been modified.
# Don't try to run python from /usr/bin/python, just run "python" and
# let the PATH figure out which version to run (based on what your
# virtualenv has configured).

python main.py
