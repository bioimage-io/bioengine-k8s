## Deploy on GKE

Follow the instructions to install https://cloud.google.com/sdk/docs/install-sdk#deb

Install google cloud cli and also google-cloud-cli-gke-gcloud-auth-plugin:
```
sudo apt-get update && sudo apt-get install google-cloud-cli
sudo apt-get install google-cloud-cli-gke-gcloud-auth-plugin
```

Install kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-kubectl-binary-with-curl-on-linux

Install helmsman and Helm

```
curl -L https://github.com/Praqma/helmsman/releases/download/v3.17.0/helmsman_3.17.0_linux_amd64.tar.gz | tar zx

mv helmsman /usr/local/bin/helmsman

curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```


```
make gke.dev
```


```
curl https://dev.hypha.bioimage.io/ -k
```