# Objective

In this series of exercises, you will learn how to deploy your code to [Google Cloud Platform](https://cloud.google.com/) aka **GCP** and in particular how to use **[AI Platform](https://cloud.google.com/ai-platform/)** in order to leverage the power of distributed computing and speedup your ML experimentation.

Beyond training models, you will see how you can make your models available to the world, manage different versions and serve predictions at scale.


# GCP Setup

## Project setup
- Go to [Google Cloud](https://console.cloud.google.com/) and create an account if you do not already have one.
- In the Cloud Console, on the project list, select or create a Cloud project. You can name it `Wagon Bootcamp` for example
- Notice the `ID` automatically created for the project. If you used the suggestion for the project name, it should look like `wagon-bootcamp-123456`. This `PROJECT_ID` will be refered to later and used all over the code in order to identify the GCP project your code will be interacting with. You will be able to access it anytime in the project list (click to zoom):

<a href="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gcp-show-project-id.png">
  <img src="https://raw.githubusercontent.com/lewagon/data-images/master/DE/gcp-show-project-id.png" width="450" alt="finding your PROJECT_ID in GCP">
</a>

- Make sure that billing is enabled for your Google Cloud project. Don't worry, as a first time user, you have a **$300 credit** to use for Google Cloud resources, which will be more than enough for this project.
- [Enable the AI Platform Training & Prediction and Compute Engine APIs.](https://console.cloud.google.com/flows/enableapi?apiid=ml.googleapis.com,compute_component&_ga=2.269215094.662509797.1580849510-2071889129.1567861089&_gac=1.154971594.1580849512.CjwKCAiAyeTxBRBvEiwAuM8dnbZ6uMwizbZW44J2mBCX6ncEjwjwpgF8S8QsvhYAXLkJ8awDnIRTNRoCJ_0QAvD_BwE) This step may take a few minutes.

## Install Cloud sdk

We need to install a new cli called gcloud. Once you are authenticated, this tool will allow you to perform any operation on the GCP platform from the command line.

### MacOSX

```bash
brew install --cask google-cloud-sdk
```

Then run this command:

```bash
/usr/local/Caskroom/google-cloud-sdk/latest/google-cloud-sdk/install.sh
```

**Restart** your terminal.

### Ubuntu/WSL2

```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get install apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-sdk
sudo apt-get install google-cloud-sdk-app-engine-python
```
👉 [Install documentation](https://cloud.google.com/sdk/docs/install#deb)


## Configure Cloud sdk
- Authenticate the gcloud tool with the google account you used for GCP. This will open a browser tab for authentication to your google account
```bash
gcloud auth login
```
- Check your active account. This should display the email address of the google account you used for GCP
```bash
gcloud auth list
```
- Set your current project (replace PROJECT_ID). This will be meaningful once you have multiple projects on GCP.
```bash
gcloud config set project PROJECT_ID
```
- Check your active account and current project
```bash
gcloud config list
```

ℹ️ Alternatively, you can use the `gcloud init` command if you want to be guided through these steps.


## Create a service account key 🔑
Now that you have created a `GCP account` and a `project` (identified by its `PROJECT_ID`), we are going to configure the actions (API calls) that you want to allow your code to perform.

Since API calls are not free, it may be important to define these with caution, but for the purpose of the bootcamp this will not be an issue and we are going to allow our code to use all API without any restrictions (see the project owner part later).

As there may be several projects associated with a GCP account, a project may be composed of several services (any bundle of code, whatever its form factor, that requires the usage of GCP API calls in order to fulfill its purpose).

GCP requires that the services of the project using API calls are registered on the platform and their credentials configured.

Here we will only need to use a single service and will create the corresponding `service account`.

Since the [service account](https://cloud.google.com/iam/docs/service-accounts) is what identifies your application (and therefore your GCP billing account and ultimately your credit card) when it comes to bill the performed API calls, you are going to want to be cautious with the next steps. Basically, do not let your service account json file by the coffee machine, do not send it as a tweet, do not store it in your git codebase (even if your git repository is private).

📣 **This step is particularly important** 📣

It is the daily challenge of every data engineer: storing 🔑 to access our 🌩️ products.
Make sure you understand what you do there and overall why you do it:
- Go to [Service Account key page](https://console.cloud.google.com/apis/credentials/serviceaccountkey)
- Click on `+ Create Service Account`:
  - Give a name to that account. Click on `Create`
  - In the "Role" dropdown, select `Owner`. Click on `Continue`
  - Click on `Done`
  - Locate your service account and click on the 3 dots on the right and click on `Manage Keys`
  - Click on `Create new key`
  - Select `JSON`. Click on `Create`
  - Download the `JSON` file, and store it somewhere you'll remember, for example:
    - macOS :point_right: `/Users/YOUR_USER_NAME/Documents/gcp_keys/YOUR_FILENAME_FOR_SECRET_KEY.json`
    - Ubuntu / WSL2 :point_right: `/home/YOUR_USER_NAME/Documents/gcp_keys/YOUR_FILENAME_FOR_SECRET_KEY.json`
  - Avoid using spaces in the name of the file, it will be easier to use it

⚠️ **MOST IMPORTANT STEP** ⚠️

You will define a new env variable called `GOOGLE_APPLICATION_CREDENTIALS`, referring to the path where you stored your secret key.
Every time you'll want to interact with GCP products, either via cli interface or with any python official gcp package, you program will look for the `GOOGLE_APPLICATION_CREDENTIALS` env variable to find the secret key path on your computer.
Last thing, make sure that the path you indicate is the **absolute path**, ie `/Users/YOUR_USER_NAME/Documents/gcp_keys/YOUR_FILENAME_FOR_SECRET_KEY.json` and not `~/Documents/gcp_keys/YOUR_FILENAME_FOR_SECRET_KEY.json`
- Add the following line to your `~/.aliases`:
  - for macOSX
  ```
  export GOOGLE_APPLICATION_CREDENTIALS=/Users/YOUR_USER_NAME/Documents/gcp_keys/YOUR_FILENAME_FOR_SECRET_KEY.json
  ```
  - for Ubuntu / WSL2

  ```
  export GOOGLE_APPLICATION_CREDENTIALS=/home/YOUR_USER_NAME/Documents/gcp_keys/YOUR_FILENAME_FOR_SECRET_KEY.json
  ```

- **Restart** your terminal and run:
```bash
echo $GOOGLE_APPLICATION_CREDENTIALS
```
expected ouptut:
```bash
/Users/YOUR_USER_NAME/Documents/gcp_keys/YOUR_FILENAME_FOR_SECRET_KEY.json
```

You should now be able to see the created service account and its role from the cli:
- List the service accounts associated to your active account and current project
```bash
gcloud iam service-accounts list
```
- Retrieve the service account email address (it was built from your project id and the service account name you entered and should look something like `SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com`)
- List the roles of the service account from the cli (replace PROJECT_ID and SERVICE_ACCOUNT_EMAIL)
```bash
gcloud projects get-iam-policy PROJECT_ID \
--flatten="bindings[].members" \
--format='table(bindings.role)' \
--filter="bindings.members:SERVICE_ACCOUNT_EMAIL"
```
- You should see that your service account has a role of roles/owner

Now your setup is complete : you used a `google account` to access the GCP platform, created a `project`, and a service account json key file which allows your code to use GCP APIs and is safely stored on your machine.

🚀 Congrats!

### Troubleshooting

`AccessDeniedException: 403 The project to be billed is associated with an absent billing account.`

- Make sure that billing is enabled for your Google Cloud Platform project.
https://cloud.google.com/billing/docs/how-to/modify-project


# Upload file to Google Cloud Storage

Now that you have a working setup, we are going to start using the products provided by the GCP platform. GCP provides tens of products, but we will be interested mainly by 2 products : `Storage`, and `AI Platform`.

In order to navigate quickly in GCP, you should scroll through the list of products in the left pane and maybe pin the most used ones (using the pin icon): `AI Platform`, `Storage`.

## Storage

`Storage` provides the capability of hosting your files online in containers called `buckets`. We will use it in order to store our train and test files, and our trained models.

You can consider that the bucket is like a disk or flash drive that would be accessible anywhere in the world, and is identified by its `BUCKET_NAME`. Inside the bucket, you can organize your data in directories (folders) and subdirectories as you would any disk or flash drive.

## AI Platform

`AI Platform` provides the capability to train your models online and/or to use trained models in order to perform predictions online.

## Bucket setup

For now, lets play with the `Storage` `buckets` in order to make sure that everything works.

You will need a bucket to store data, code and trained models.

⚠️ **IMPORTANT**: Bucket names must be **globally unique**, please respect convention `wagon-ml-[YOUR_LAST_NAME]-[BATCH_NUMBER]`

As the `PROJECT_ID` is used in your code in order to identify your project, the `BUCKET_NAME` will be used in your code to identify this online container where you will store your data and your models.

You can list the buckets of your project in [Navigation menu / Storage / Browser](https://console.cloud.google.com/storage/browser).

💡 Use the `train_1k.csv` training file in order to test the upload and the model training quickly. Eventually you are going to want to upload the full dataset in order to create a better model.

First, we will download the `train_1k.csv` file:

``` bash
curl --silent 'https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_1k.csv' > ~/code/<user.github_nickname>/TaxiFareModel/raw_data/train_1k.csv
```

You will need to reference the location of the file in your code.

<details>
<summary>
  💡 Hint: how to find the local path to <code>train_1k.csv</code>?
</summary>


  From your terminal, go to the TaxiFareModel project that you created yesterday:

  ``` bash
  cd ~/code/<user.github_nickname>/TaxiFareModel
  ```

  From there, go to the <code>raw_data</code> directory. You should see the [train_1k.csv](https://wagon-public-datasets.s3.amazonaws.com/taxi-fare-ny/train_1k.csv) file inside.

  In order to reference it, print the local path with <code>pwd</code>.
</details>

There are 2 ways to create a bucket:

### The hacker's way (**recommended**)

- Open `Makefile` in your `TaxiFareModel` project and copy the following lines.

```make
# project id - replace with your Project's ID
PROJECT_ID=XXX

# bucket name - follow the convention of wagon-ml-[YOUR_LAST_NAME]-[BATCH_NUMBER]
BUCKET_NAME=XXX

# Choose your region https://cloud.google.com/storage/docs/locations#available_locations
REGION=europe-west1

set_project:
    @gcloud config set project ${PROJECT_ID}

create_bucket:
    @gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}
```

We need to fix the indentations as you copied the code with __spaces__ and we need to replace them with __tabs__. If you don't do it you'll probably see an error about `missing separator` while running the commands. If you can't figure it out yourself, make a ticket.

- Use the predefined bash commands from `Makefile` to create your bucket

```bash
make set_project
make create_bucket
```

👉 Check on [Storage](https://console.cloud.google.com/storage) that your bucket has been created.

### The UI way (just to know)

- Go to [Storage](https:A//console.cloud.google.com/storage) and create a bucket from there
- Select `Location type`: `Region` since we will not need to access our bucket from all over the world
- Bucket should be created in the nearest region (`europe-west1` for France)
- Keep other options default

## Upload your dataset

- Add the following lines to your `Makefile` (don't forget about the indentation!)

```make
# path of the file to upload to gcp (the path of the file should be absolute or should match the directory where the make command is run)
LOCAL_PATH="XXX" # Replace with your local path to the `train_1k.csv` and make sure to put it between quotes

# bucket directory in which to store the uploaded file (we choose to name this data as a convention)
BUCKET_FOLDER=data

# name for the uploaded file inside the bucket folder (here we choose to keep the name of the uploaded file)
# BUCKET_FILE_NAME=another_file_name_if_I_so_desire.csv
BUCKET_FILE_NAME=$(shell basename ${LOCAL_PATH})

upload_data:
    # @gsutil cp train_1k.csv gs://wagon-ml-my-bucket-name/data/train_1k.csv
    @gsutil cp ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}
```

- Finally use the predefined bash command from `Makefile` to upload your file to

```bash
make upload_data
```

👉 Check on [Storage](https://console.cloud.google.com/storage) that your file was correctly uploaded. You should see a `train_1k.csv` file in the `data` folder of your bucket. Look at the content of the `Makefile`. Can you see how the command used in order to upload the file is built ?

🚀 Congrats!
