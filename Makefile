SSH_KEY_PATH ?= $${HOME}/.ssh/id_rsa
IMAGE_NAME ?=  "fwork/lead_service"
ADDITIONAL_DOCKER_BUILD_ARGS ?=

# Version is a git tag name for current SHA commit hash or this hash if tag is not presented
APP_VERSION ?= $$(git describe --exact-match --tags $(git log -n1 --pretty='%h') 2> /dev/null || \
				  git log -n1 --pretty='commit_sha:%h')

vars:
	@echo IMAGE_NAME=${IMAGE_NAME}
	@echo SSH_KEY_PATH=${SSH_KEY_PATH}
	@echo ADDITIONAL_DOCKER_BUILD_ARGS=${ADDITIONAL_DOCKER_BUILD_ARGS}
	@echo APP_VERSION=${APP_VERSION}

image:
	docker build --pull -f build/Dockerfile -t ${IMAGE_NAME} . --force-rm=True \
								 --build-arg rsakey="$$(cat ${SSH_KEY_PATH})" \
								 --build-arg APP_VERSION=${APP_VERSION} \
								 ${ADDITIONAL_DOCKER_BUILD_ARGS}

image_dev:
	docker build --pull -f build/Dockerfile -t ${IMAGE_NAME} . --force-rm=True \
							     --build-arg rsakey="$$(cat ${SSH_KEY_PATH})"\
							     --build-arg isdev="1" \
								 --build-arg APP_VERSION=${APP_VERSION} \
								 ${ADDITIONAL_DOCKER_BUILD_ARGS}

compose_config:
	docker-compose -f ./build/docker-compose.test.yml config

run:
	docker-compose -f ./build/docker-compose.yml up web_lead

test: compose_config clean
	docker-compose -f ./build/docker-compose.test.yml up --renew-anon-volumes --abort-on-container-exit

test_local:
	docker-compose -f ./build/docker-compose.test.yml -f ./build/docker-compose.test_local.yml up --renew-anon-volumes --abort-on-container-exit

clean:
	docker-compose -f ./build/docker-compose.yml down
	docker-compose -f ./build/docker-compose.test.yml rm -s -v -f
	docker-compose -f ./build/docker-compose.yml rm -s -v -f

push_to_registry: image
	docker push ${IMAGE_NAME}