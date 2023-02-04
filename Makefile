path = server

check_code:
	autoflake -i -r --remove-all-unused-imports $(path)
	black --line-length=100 $(path)
	isort $(path)
	flake8 --show-source $(path)
	mypy --strict $(path)

server/dev:
	uvicorn server.api:app \
		--reload \
		--host 0.0.0.0 \
		--port 8000
