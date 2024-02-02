# hypha-k8s
## Kubernetes deployment

Deployment is managed by helmsman v3.6.3 on kubernetes 1.22:

    https://github.com/Praqma/helmsman

MacOS:

    brew install helmsman

Important deployment values can be found in helmsman/hypha.yaml

Full production deployment using helmsman (includes ingress, gpu-operator, nvidia device plugin):

    helmsman --debug -f helmsman.yaml --dry-run
    helmsman --debug -f helmsman.yaml --apply

Dev only deployment:

    helmsman --debug --group dev -f helm-chart/helmsman.yaml --dry-run

	helmsman --debug --group dev -f helm-chart/helmsman.yaml --apply


