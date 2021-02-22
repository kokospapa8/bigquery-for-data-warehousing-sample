# Chapter 11 CLI Code
## Create Cloud functions with GCS trigger
```
gcloud functions deploy {your_function_name} \
--trigger-resource {GOOGLE_CLOUD_STORAGE_BUCKET_NAME} \
--trigger-event google.storage.object.finalize

```
