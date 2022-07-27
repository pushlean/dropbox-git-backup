pin-dependencies:
	poetry export -f requirements.txt --output requirements.txt
test:
	docker compose run sync pytest
