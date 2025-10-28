#!/bin/bash
set -e  # stop on first error

# Start main.py (your backend) in background
python3 main.py &

# Start streamlit in foreground so container stays alive
streamlit run app.py --server.port=8501 --server.address=0.0.0.0