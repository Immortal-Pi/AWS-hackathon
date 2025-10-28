#!/bin/bash
set -e  # stop on first error

# Start main.py (your backend) in background
python main.py &

# Start streamlit in foreground so container stays alive
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0