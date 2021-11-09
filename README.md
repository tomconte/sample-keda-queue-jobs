# KEDA jobs with Azure Storage Queues
### based on https://github.com/tomconte/sample-keda-queue-jobs but substantially modified

These samples show how to use [KEDA](https://github.com/kedacore/keda) to automatically schedule Kubernetes workloads based on an Azure Storage Queue trigger.

## Sample #1 - Linux nodes, ephemeral disks, workloads scheduled as  jobs
This sample creates an AKS cluster with an ephemeral-disk linux node pool.

See [script-job.sh] and [azurequeue_scaledobject_jobs.yaml]

## Sample #2 - Linux nodes, managed disks with deallocate scaledown, workloads scheduled as jobs

Note:  Be sure to delete the cluster from sample 1, or at least the keda scaled object so that the two jobs dont compete (they use the same queue)

see [script-job-deallocate.sh]  and [azurequeue_scaledobject_jobs.yaml]



## Sample #3 - Windows nodes, managed disks with deallocate scaledown, workloads scheduled as jobs

see [./script-windows.sh]  and [azurequeue_scaledobject_jobs_windows.yaml]


