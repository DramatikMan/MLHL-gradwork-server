path = gwserver

check_code:
	autoflake -i -r --remove-all-unused-imports $(path)
	black --line-length=100 --exclude='migrations' $(path)
	isort $(path)
	flake8 --show-source --exclude migrations $(path)
	mypy --strict $(path)

server/dev:
	uvicorn gwserver.api:app \
		--reload \
		--host 0.0.0.0 \
		--port 8000
