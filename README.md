# KEDA jobs with Azure Storage Queues

This sample shows how to use [KEDA](https://github.com/kedacore/keda) to automatically schedule Kubernetes Jobs based on an Azure Storage Queue trigger.

## Create an Azure Storage Queue

Using the Azure CLI, create a Resource Group, a Storage Account, and a Queue:

```
STORAGE_ACCOUNT_NAME=storageaccountname
export QUEUE_NAME=keda-queue
az group create -l westus -n hello-keda
az storage account create -g hello-keda -n $STORAGE_ACCOUNT_NAME
export AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string --name $STORAGE_ACCOUNT_NAME --query connectionString -o tsv)
az storage queue create -n $QUEUE_NAME
```

You will need to choose a unique name for the `STORAGE_ACCOUNT_NAME` variable.

## Build and push the queue consumer container image

The `queue-consumer` directory contains a simple Python script that consumes a single message from an Azure Storage Queue and sleeps for 30 seconds, simulating a very simple job.

The script requires two environment variables:

- `AzureWebJobsStorage`: the Azure Storage connection string you obtained from the previous step.
- `QUEUE_NAME`: the name of the queue to read from.

To schedule the jobs, you will need to build and push the Docker image to a container registry. For exanple, to use Docker Hub:

```
export REGISTRY=tomconte
cd queue-consumer/
docker build -t queue-consumer .
docker tag queue-consumer $REGISTRY/queue-consumer
docker push $REGISTRY/queue-consumer
```

Replace the value for `REGISTRY` with your own Docker hub profile name.

## Install KEDA

[Follow the instructions](https://github.com/kedacore/keda#setup) to deploy KEDA on your Kubernetes cluster.

## Create the KEDA ScaledObject

The `azurequeue_scaledobject_jobs.yaml` YAML configuration defines the trigger and the specification of the job to run. You will need to check a few values:

- Set the container image name
- Check that the queue names are correct

You will also need to create a secret to store the Azure Storage connection string:

```
kubectl create secret generic secrets --from-literal=AzureWebJobsStorage=$AZURE_STORAGE_CONNECTION_STRING
```

You can then create the ScaledObject:

```
kubectl apply -f azurequeue_scaledobject_jobs.yaml
```

Nothing will happen right away since our queue is empty!

## Send some messages to the queue

The `send_messages.py` script can be used to send a bunch of messages to the queue. You will need to configure the `AzureWebJobsStorage` and `QUEUE_NAME` environment variables as defined above. To send e.g. a hundred messages:

```
export AzureWebJobsStorage=$AZURE_STORAGE_CONNECTION_STRING
python send_messages.py 100
```

## Watch KEDA at work

Now you can watch jobs being automatically scheduled until the queue has been drained:

```
kubectl get jobs
```
