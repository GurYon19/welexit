from platform import processor
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import FailedPrecondition
from google.cloud import documentai  # type: ignore




"""

gcloud auth application-default login

"""
# TODO(developer): Uncomment these variables before running the sample.
project_id = 'welexit-attempt'
location = 'eu' # Format is 'us' or 'eu'


def fetch_processor_types_sample(project_id: str, location: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location
    parent = client.common_location_path(project_id, location)

    # Fetch all processor types
    response = client.fetch_processor_types(parent=parent)

    print("Processor types:")
    # Print the available processor types
    for processor_type in response.processor_types:
        if processor_type.allow_creation:
            print(processor_type.type_)

def list_processors_sample(project_id: str, location: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location
    parent = client.common_location_path(project_id, location)

    # Make ListProcessors request
    processor_list = client.list_processors(parent=parent)

    # Print the processor information
    for processor in processor_list:
        print(f"Processor Name: {processor.name}")
        print(f"Processor Display Name: {processor.display_name}")
        print(f"Processor Type: {processor.type_}")
        print("")
        return processor
    
def get_processor_sample(project_id: str, location: str, processor_id: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor, e.g.:
    # projects/{project_id}/locations/{location}/processors/{processor_id}
    name = client.processor_path(project_id, location, processor_id)

    # Make GetProcessor request
    processor = client.get_processor(name=name)

    # Print the processor information
    print(f"Processor Name: {processor.name}")
    print(f"Processor Display Name: {processor.display_name}")
    print(f"Processor Type: {processor.type_}")

def enable_processor_sample(project_id: str, location: str, processor_id: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)
    request = documentai.EnableProcessorRequest(name=processor_name)

    # Make EnableProcessor request
    try:
        operation = client.enable_processor(request=request)

        # Print operation name
        print(operation.operation.name)
        # Wait for operation to complete
        operation.result()
    # Cannot enable a processor that is already enabled
    except FailedPrecondition as e:
        print(e.message)

def disable_processor_sample(project_id: str, location: str, processor_id: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)
    request = documentai.DisableProcessorRequest(name=processor_name)

    # Make DisableProcessor request
    try:
        operation = client.disable_processor(request=request)

        # Print operation name
        print(operation.operation.name)
        # Wait for operation to complete
        operation.result()
    # Cannot disable a processor that is already disabled
    except FailedPrecondition as e:
        print(e.message)

def delete_processor_sample(project_id: str, location: str, processor_id: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)
    request = documentai.DeleteProcessorRequest(name=processor_name)

    # Make DeleteProcessor request
    operation = client.delete_processor(request=request)

    # Print operation name
    print(operation.operation.name)
    # Wait for operation to complete
    operation.result()
if __name__ == "__main__":
    #fetch_processor_types_sample(project_id, location)
    processor = list_processors_sample(project_id, location)