path = app

check_code:
	autoflake -i -r --remove-all-unused-imports $(path)
	black --line-length=100 $(path)
	isort $(path)
	flake8 --show-source $(path)
	mypy --strict $(path)
