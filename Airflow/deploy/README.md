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
--machine-type e2-standard-8 \
--num-nodes 1 \
--zone asia-northeast1-a

gcloud container clusters delete $CLUSTER_NAME --zone $ZONE
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

6. Change storage class
```
kubectl patch storageclass standard-rwo -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
kubectl patch storageclass standard -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

7. Get Configuration Values
```
helm show values apache-airflow/airflow > values.yaml
```

8. Create secrect git Sync
```
kubectl create secret generic airflow-gke-git-secret --from-file=gitSshKey=airflowsshkey -n airflow

kubectl create secret generic airflow-gke-git-secret \
  --from-file=gitSshKey=airflowsshkey \
  --from-file=known_hosts=github_public_key \
  -n airflow

kubectl exec --stdin --tty airflow-webserver-588d844465-2gz6v -n airflow -- /bin/bash
```

8. 
```
kubectl cp running_python_bash_and_dummy_operator.py airflow/airflow-webserver-649f97f5cb-k86m7:/opt/airflow/dags
```

9. Update with new values
```
helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml
```

11. Prepare buckets
```
gcloud storage cp gs://data-engineer-393307-ecommerce-bucket/products-2023-08-09-converted.json gs://data-engineer-393307-cloud-data-lake
/data/

gcloud storage cp gs://data-engineer-393307-ecommerce-bucket/products-2023-08-02-converted.json gs://data-engineer-393307-cloud-data-lake
/data/
```

12. Create Service Account
```
SA_NAME=airflow-gke-sa

gcloud iam service-accounts create $SA_NAME \
    --description="Airflow GKE Service Account" \
    --display-name="Airflow GKE Service Account"

gcloud iam service-accounts keys list \
    --iam-account=$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.objectUser"
```