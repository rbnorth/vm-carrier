# vm-carrier
Moves vm's through GCP Projects

vm-carrier as came about from creating a vm in one google project and that
vm would be needed in another project.  The -h or --help displays all the 
information about using this tool. 

./vm_carrier.py

```bash
usage: vm_carrier.py [-h] --project PROJECT [--zone ZONE] --source-image SOURCE_IMAGE --service-account SERVICE_ACCOUNT --subnet SUBNET instance_name

Create a Google Compute Engine instance in another project.

positional arguments:
  instance_name         The name of the instance to create.

options:
  -h, --help            show this help message and exit.
  --project PROJECT     The Google Cloud project ID.
  --zone ZONE           The compute zone (default: us-central1-b).
  --source-image SOURCE_IMAGE
                        The source machine image (gcloud compute machine-images list --uri).
  --service-account SERVICE_ACCOUNT
                        The service account email for the instance.
  --subnet SUBNET       The subnet to deliver the vm to.
  ```