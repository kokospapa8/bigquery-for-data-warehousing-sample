# Appendix A CLI Code
## Server with ngrok
```bash
nohup python3 -m http.server 8080 > server.log 2>&1 &
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip unzip ./ngrok-stable-linux-386.zip
```

## Install SDK
```bash
curl https://sdk.cloud.google.com > install.sh
bash install.sh --disable-prompts
```

## gcloud
```bash
gcloud projects create {YOUR-PROJECT-NAME}
gcloud config set project {YOUR-PROJECT-NAME}
gcloud iam service-accounts create --account-name {YOUR_ACCOUNT_NAME} --display-name {YOUR_DISPLAY_NAME}

gcloud projects add-iam-policy-binding {YOUR_PROJECT_ID} --member serviceAccount:{YOUR_SERVICE_ACCOUNT_EMAIL} --role {ROLE_NAME}
```
## bq
```bash
bq ls
bq query “SELECT 42”
bq query --sync --format csv “SELECT ...” > results.csv
bq shell
bq mk --table dataset.table field1:string,otherfield:string
bq cp <source-table> <destination-table>
bq rm -r <dataset>
```

### bq undelete
```bash
#!/bin/bash
# Usage: bq dataset-table time-in-seconds
bq cp "$1@$((('date +%s'-$2)*1000))" $1_recovered 
```
