# Variables
COMPOSEFILE := ./srcs/docker-compose.yml
COMPOSE := docker compose -f $(COMPOSEFILE)
COLOR := \033[1;33m
RESET := \033[0m

# Default target
.DEFAULT_GOAL := build

# Phony targets declaration
.PHONY: build up down stop restart clean prune re status default

# Targets
build:
	@echo -e "$(COLOR)BUILD$(RESET)"
	@$(COMPOSE) up -d --build
	@$(COMPOSE) up

up:
	@echo -e "$(COLOR)UP$(RESET)"
	@$(COMPOSE) up

down:
	@echo -e "$(COLOR)DOWN$(RESET)"
	@$(COMPOSE) down

stop:
	@echo -e "$(COLOR)STOP$(RESET)"
	@$(COMPOSE) stop

restart:
	@echo -e "$(COLOR)RESTART$(RESET)"
	@$(COMPOSE) restart

clean:
	@echo -e "$(COLOR)CLEAN$(RESET)"
	@$(COMPOSE) down -v --rmi local

prune:
	@echo -e "$(COLOR)PRUNE$(RESET)"
	@$(COMPOSE) down -v
	@docker system prune -af
	@docker volume prune -f

re: down build

status:
	@echo -e "$(COLOR)Containers$(RESET)"
	@docker ps -a
	@echo -e "$(COLOR)Images$(RESET)"
	@docker images
	@echo -e "$(COLOR)Volumes$(RESET)"
	@docker volume ls
	@echo -e "$(COLOR)Networks$(RESET)"
	@docker network ls

# Make build the default target
default: build