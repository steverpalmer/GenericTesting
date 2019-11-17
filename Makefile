init:
    pip install -r requirements.txt

test:
    python -m unittest tests/test_*

.PHONY: init test
