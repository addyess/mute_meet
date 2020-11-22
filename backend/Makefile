venv/bin/activate:
	virtualenv -m python3 venv

.PHONY: prepare
prepare: venv/bin/activate requirements.txt
	( \
		source venv/bin/activate; \
		pip install -r requirements.txt; \
	)

.PHONY: run
run:
	( \
		source venv/bin/activate; \
		python3 -m backend; \
	)

