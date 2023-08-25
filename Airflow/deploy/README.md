1. Prepare the evironment variables
```
PROJECT_ID=`gcloud config get-value project`
SERVICE_ACCOUNT=$(gsutil kms serviceaccount)
REGION=asia-northeast1
ZONE=asia-northeast1-a

CLUSTER_NAME=airflow-cluster
```

2. Install
```
sudo apt-get install kubectl
kubectl version

sudo apt-get install helm
helm version

sudo apt-get install google-cloud-sdk-gke-gcloud-auth-plugin
gke-gcloud-auth-plugin --version
```

3. Create GKE Cluster
```
gcloud container clusters create $CLUSTER_NAME \
--machine-type e2-medium \
--num-nodes 1 \
--zone asia-northeast1-a
```

3. Update using plugin
```
gcloud container clusters get-credentials $CLUSTER_NAME --zone=$ZONE
```

4. Add repo by Helm
```
helm repo add apache-airflow https://airflow.apache.org
helm repo list
```


5. Create the namespace Airflow
```
kubectl create namespace airflow
helm upgrade --install airflow apache-airflow/airflow -n airflow --debug
```

6. Authentication
```
Airflow Webserver:     kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
Default Webserver (Airflow UI) Login credentials:
    username: admin
    password: }5S\bqDdt%pxj?_H
Default Postgres connection credentials:
    username: postgres
    password: postgres
    port: 5432
```

7. Create secrect git Sync
```
kubectl create secret generic airflow-gke-git-secret --from-file=gitSshKey=airflowsshkey -n airflow
```