# Makefile

BASEDIR = $(shell pwd)

VARIANTS := embassy denbi minikube
ENVIRONMENTS := prod dev local

.PHONY: all $(VARIANTS) $(ENVIRONMENTS) $(VARIANTS:%=%.prod) $(VARIANTS:%=%.dev) htpassword

all: $(VARIANTS)

$(VARIANTS): %:
	@echo "Deploying $@..."
	$(MAKE) $@.prod
	$(MAKE) $@.dev

$(ENVIRONMENTS): %:
	@echo "Deploying to $@..."
	ENV_FILE="$*.$@.env"
	$(MAKE) $(VARIANTS:%=%.$@)

$(VARIANTS:%=%.prod): %.prod:
	@echo "Deploying $* to prod..."
	helmsman --apply --debug --group "prod" -f helmsman.yaml -e $*.prod.env --subst-env-values

$(VARIANTS:%=%.dev): %.dev:
	@echo "Deploying $* to dev..."
	helmsman --apply --debug --group "dev" -f helmsman.yaml -e $*.dev.env --subst-env-values

$(VARIANTS:%=%.local): %.local:
	@echo "Deploying $* to local..."
	helmsman --apply --debug --group "prod" -f helmsman.yaml -f helmsman/local.yaml -e $*.local.env --subst-env-values

htpassword:
	docker run --rm -ti xmartlabs/htpasswd ${CI_REGISTRY_USER} ${CI_REGISTRY_PASSWORD} > htpasswd_file
	cat htpasswd_file


set.dot.env:
	set -o allexport; source ./secrets.env; set +o allexport
local.test:
	act --secret-file secrets.yaml


# prod:
# 	helmsman --debug -f helmsman.yaml --subst-env-values --apply
# staging:
# 	helmsman --debug --group staging -f helmsman.yaml --subst-env-values --apply
# staging.dry:
# 	helmsman --debug --group staging -f helmsman.yaml --subst-env-values --dry-run
