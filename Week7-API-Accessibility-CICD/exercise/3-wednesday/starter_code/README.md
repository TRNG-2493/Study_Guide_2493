# Wednesday starter code

    pip install -r requirements.txt
    python project2_api_server.py 8000          # terminal 1 (restart it for a clean slate)
    pytest -p no:randomly                        # terminal 2: baseline passes in file order
    pytest -p randomly                           # ...and now watch it break

The baseline suite in tests/api/ is deliberately messy. app/price_service.py is the code under test for Stage 6; do not edit it.
