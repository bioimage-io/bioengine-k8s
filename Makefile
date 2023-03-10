BASEDIR = $(shell pwd)

VARIANTS := embassy denbi minikube gke
ENVIRONMENTS := prod dev local

.PHONY: all deploy htpassword set.dot.env local.test

all: $(VARIANTS)

define DEPLOY_template =
deploy-$(1)-$(2):
	@echo "Deploying $(1) to $(2)..."
	helmsman --apply --debug --group "$(2)" -f helmsman.yaml -e $(1).$(2).env --subst-env-values
endef

$(foreach variant,$(VARIANTS),$(foreach env,$(ENVIRONMENTS),$(eval $(call DEPLOY_template,$(variant),$(env)))))

htpassword:
	docker run --rm -ti xmartlabs/htpasswd ${CI_REGISTRY_USER} ${CI_REGISTRY_PASSWORD} > htpasswd_file
	cat htpasswd_file

prod:
	helmsman --debug -f helmsman.yaml --subst-env-values --apply --always-upgrade
staging:
	helmsman --debug --group staging -f helmsman.yaml --subst-env-values --apply --always-upgrade
staging.dry:
	helmsman --debug --group staging -f helmsman.yaml --subst-env-values --dry-run --always-upgrade
set.dot.env:
	set -o allexport; source ./secrets.env; set +o allexport

local.test:
	act --secret-file secrets.yaml
In this setup:
