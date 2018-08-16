default: start

.PHONY: deploy
deploy: push
	eval $$(docker-machine env clashstats --shell bash); docker-compose -f docker-compose.yml pull
	eval $$(docker-machine env clashstats --shell bash); docker-compose -f docker-compose.yml -f docker-compose.production.yml -p clashstats up -d --remove-orphans

.PHONY: build
build:
	docker-compose -f docker-compose.yml build --build-arg SOURCE_COMMIT=$$(git rev-parse --short HEAD) web

.PHONY: push
push: TAG=$(shell cat package.json | jq -r .version)
push: build
	docker tag amir20/clashleaders amir20/clashleaders:$(TAG)
	docker push amir20/clashleaders:$(TAG)
	docker push amir20/clashleaders:latest

.PHONY: init
init:
	pip install .[test]

.PHONY: test
test:
	python setup.py test

.PHONY: start
start:
	@npm start

.PHONY: release_patch
release_patch:
	@npm version patch

.PHONY: release_minor
release_minor:
	@npm version minor


