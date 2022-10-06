#!/usr/bin/make

include .env

SHELL = /bin/sh

MAIN_COMPOSE=docker-compose.yml
PGADMIN_COMPOSE=./tools/pgadmin4/docker-compose.yml
COMPOSES=-f $(MAIN_COMPOSE) -f $(PGADMIN_COMPOSE)

ifeq ($(DEVELOPMENT), True)
	CURRENT_UID := $(shell id -u):$(shell id -g)
	IMAGES := nginx-unit
else
	CURRENT_UID := $(USER_ID):$(USER_GROUP_ID)
	IMAGES := $(POSTGRES_CONTAINER_NAME)
endif

define SERVERS_JSON
{
	"Servers": {
		"1": {
			"Name": "Trasan Main",
			"Group": "Servers",
			"Host": "$(POSTGRES_HOST)",
			"Port": 5432,
			"MaintenanceDB": "$(POSTGRES_DB)",
			"Username": "$(POSTGRES_SU)",
			"SSLMode": "prefer",
			"PassFile": "/tmp/pgpassfile"
		}
	}
}
endef 

export PGPASS
export SERVERS_JSON
export CURRENT_UID
export IMAGES
export BACKEND_CONTAINER

up:
	docker build -f base/Dockerfile -t $(COMPOSE_PROJECT_NAME)_base ./base/
	# docker volume create $(COMPOSE_PROJECT_NAME)_$(POSTGRES_VOLUME_DATA_NAME)
	docker compose -f $(MAIN_COMPOSE) up -d --force-recreate --build --remove-orphans $(IMAGES)
down:
	docker compose $(COMPOSES) down
psql:
	docker exec -e PGPASSWORD=$(POSTGRES_SU_PASS) -it $(POSTGRES_CONTAINER_NAME) \
	psql -d $(POSTGRES_DB) -h $(POSTGRES_HOST) -p 5432 -U $(POSTGRES_SU)
pgadmin:
	rm -f ./tools/pgadmin4/servers.json
	echo "$$SERVERS_JSON" > ./tools/pgadmin4/servers.json
	docker volume create $(COMPOSE_PROJECT_NAME)_$(POSTGRES_VOLUME_DATA_NAME)
	docker volume create ${COMPOSE_PROJECT_NAME}_${PGADMIN_VOLUME_NAME}
	docker compose $(COMPOSES) up -d --build --remove-orphans $(PGADMIN_CONTAINER_NAME)
logs:
	docker compose $(COMPOSES) logs -f
clear:
	docker volume rm $(COMPOSE_PROJECT_NAME)_$(POSTGRES_VOLUME_DATA_NAME) -f
	docker volume rm ${COMPOSE_PROJECT_NAME}_${PGADMIN_VOLUME_NAME} -f
	rm -f ./tools/pgadmin4/servers.json
 