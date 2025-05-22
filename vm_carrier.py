#!/usr/bin/env python

import argparse
import subprocess
from functools import wraps
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_execution(func):
    """
    Decorator to log the execution of a function.
    Logs the start, arguments, and completion of the function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Executing: {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"Completed: {func.__name__}")
        return result
    return wrapper

def validate_inputs(func):
    """
    Decorator to validate inputs for the create_instance function.
    Ensures that all required parameters are provided and meet basic criteria.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the parameters
        instance_name = kwargs.get('instance_name')
        project = kwargs.get('project')
        zone = kwargs.get('zone')
        source_image = kwargs.get('source_image')
        service_account = kwargs.get('service_account')
        subnet = kwargs.get('subnet')

        # Perform basic validations
        if not instance_name or len(instance_name) > 63:
            logging.error("Instance name must be non-empty and no longer than 63 characters.")
            raise ValueError("Instance name must be non-empty and no longer than 63 characters.")
        if not project:
            logging.error("Project ID is required.")
            raise ValueError("Project ID is required.")
        if not zone:
            logging.error("Zone is required.")
            raise ValueError("Zone is required.")
        if not source_image:
            logging.error("Source image URI is required.")
            raise ValueError("Source image URI is required.")
        if not service_account:
            logging.error("Service account email is required.")
            raise ValueError("Service account email is required.")
        if not subnet:
            logging.error("Subnet is required.")
            raise ValueError("Subnet is required.")
            
        logging.info("Input validation passed.")
        return func(*args, **kwargs)
    return wrapper

@log_execution
@validate_inputs
def create_instance(instance_name, project, zone, source_image, service_account, subnet):
    """
    Create a Google Compute Engine instance using the gcloud CLI.

    Args:
        instance_name (str): The name of the instance to create.
        project (str): The Google Cloud project ID.
        zone (str): The compute zone to deploy the instance in (e.g., us-central1-b).
        source_image (str): The source machine image to use for the instance.
        service_account (str): The service account email for the instance.
        subnet (str): The subnet to use for the instance.

    Raises:
        subprocess.CalledProcessError: If the gcloud command fails.
    """

    # Construct the gcloud command to create an instance
    command = [
        "gcloud", "compute", "instances", "create", instance_name,
        f"--project={project}",
        f"--zone={zone}",
        f"--source-machine-image={source_image}",
        f"--service-account={service_account}",
        f"--subnet={subnet}"
    ]
    
    # Print the command being run for clarity
    try:
        logging.info(f"Running command: {' '.join(command)}")
        # Execute the command
        subprocess.run(command, check=True)
        logging.info(f"Instance {instance_name} created successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while creating instance: {e}")
        raise

def main():
    """
    Main function to parse command-line arguments and create a Google Compute Engine instance.

    Command-line flags:
    - instance_name: The name of the instance to create.
    - --project: The Google Cloud project ID (required).
    - --zone: The compute zone (default: us-central1-b).
    - --source-image: The source machine image (required).
    - --service-account: The service account email for the instance (required).
    - --subnet: The subnet to use for the instance (required).
    """
    
    # Set up the argument parser for the CLI
    parser = argparse.ArgumentParser(description="Create a Google Compute Engine instance in another project.")
    
    # Positional argument for the instance name
    parser.add_argument("instance_name", help="The name of the instance to create.")
    
    # Required arguments for project, zone (with a default), source image, service account, and subnet
    parser.add_argument("--project", required=True, help=(
        '''The Google Cloud project ID.'''))
    
    # Setting default zone as 'us-central1-b'
    parser.add_argument("--zone", default="us-central1-b", help="The compute zone (default: us-central1-b).")

    parser.add_argument("--source-image", required=True, help="The source machine image (gcloud compute machine-images list --uri).")
    
    # Adding help text for the service account with predefined options
    parser.add_argument("--service-account", required=True, help=(
        '''The service account email for the instance.'''))
    
    # Required subnet argument
    parser.add_argument("--subnet", required=True, help="The subnet to deliver the vm to.")
    
    # Parse the arguments from the command line
    args = parser.parse_args()
    
    logging.info("Parsed command-line arguments successfully.")
    
    # Call the function to create the instance with the provided arguments
    create_instance(
        instance_name=args.instance_name,
        project=args.project,
        zone=args.zone,
        source_image=args.source_image,
        service_account=args.service_account,
        subnet=args.subnet
    )

if __name__ == "__main__":
    logging.info("Starting the script execution.")

    # Entry point of the script
    main()

    logging.info("Script execution completed.")
