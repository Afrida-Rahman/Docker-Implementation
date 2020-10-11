#Production 
start:
	docker container start db_mongo api_flask
build:
	./boot.sh
stop:
	docker container stop api_flask db_mongo
destroy: stop
	docker network rm flask-mongo-network
	docker container rm api_flask db_mongo
	docker image rm api_flask

#Development
dev-start:
	docker-compose up --detach
dev-build:
	docker-compose up --detach --build;
dev-shell:
	docker-compose exec api bash
dev-stop:
	docker-compose stop
dev-destroy:
	docker-compose down --volume