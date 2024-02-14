import os
import re
import json
from typing import LiteralString, Optional
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

curr_dir = os.getcwd()
data_dir = os.path.join(curr_dir, "data")
pdf_files = os.listdir(os.path.join(curr_dir, "data", "pdf_files"))

def find_tags(text,tags) -> LiteralString:
    #add docstring
    """
    This function finds the tags in the text
    """
    file_tags = find_tags_regex(text,tags)
    #convert file_tags to string
    file_tags = ",".join(file_tags)
    return file_tags

def process_document_sample(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
    field_mask: Optional[str] = None,
    processor_version_id: Optional[str] = None,
) -> str:
    """
    This function processes the document using the Document AI API.
    It returns the text extracted from the document.
    It uses the `process_document` method of the `DocumentProcessorServiceClient` class.
    It takes in the following arguments:
    - project_id: The ID of the Google Cloud project.
    - location: The location of the Document AI processor.
    - processor_id: The ID of the Document AI processor.
    - file_path: The path to the file to process.
    - mime_type: The MIME type of the file.
    - field_mask: The field mask to specify which fields to return.
    - processor_version_id: The ID of the Document AI processor version.
    """
    # You must set the `api_endpoint` if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    if processor_version_id:
        # The full resource name of the processor version, e.g.:
        # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
        name = client.processor_version_path(
            project_id, location, processor_id, processor_version_id
        )
    else:
        # The full resource name of the processor, e.g.:
        # `projects/{project_id}/locations/{location}/processors/{processor_id}`
        name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # For more information: https://cloud.google.com/document-ai/docs/reference/rest/v1/ProcessOptions
    # Optional: Additional configurations for processing.
    process_options = documentai.ProcessOptions(
        # Process only specific pages
        # individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
        #     pages=[1]
        # )
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
        field_mask=field_mask,
        process_options=process_options,
    )

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    document = result.document
    text = document.text
    return text

def find_tags_regex(text, tags):
  "returns tags found in text in the fastest way"
  regex = "|".join(tags)
  return set(re.findall(regex, text, flags=re.IGNORECASE))

def get_text_from_pdf(pdf_name) -> str:
    """
    This function gets the text from the pdf file
    pdf_name: name of the pdf file without the extension
    returns: text from the pdf file

    """
    # this for ocr
    project_id = 'welexit-attempt'
    location = 'eu' # Format is 'us' or 'eu'
    processor_id = "823b06a76761e433" # Create processor before running sample
    mime_type = "application/pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
    # field_mask = "text,entities,pages.pageNumber"  # Optional. The fields to return in the Document object.
    # processor_version_id = "YOUR_PROCESSOR_VERSION_ID" # Optional. Processor version to use
    pdf_folder = os.path.join(data_dir, "pdf_files")
    file_path = os.path.join(pdf_folder,pdf_name)
    return process_document_sample(project_id,location,processor_id,file_path,mime_type)

def save_dict_to_json(dict_to_save, filename) -> None:
    with open(filename, "w") as f:
        json.dump(dict_to_save, f)

def get_tags_from_xlsx(filename)->list:
    """
    This function gets the tags from the xlsx file
    filename: name of the xlsx file
    returns: list of tags from the xlsx file
    """
    tags_df = pd.read_excel(filename)
    tags = tags_df.iloc[:,0].tolist()
    return tags
    
if __name__ == "__main__":
    """
    example how to use this functions
    """
    #create tags list from xlsx
    tags_filename = os.path.join(data_dir, "keywords.xlsx") 
    all_tags = get_tags_from_xlsx(tags_filename)
    
    tags_dict = {}
    for pdf_file in pdf_files:
        text = get_text_from_pdf(pdf_file)
        tags = find_tags(text, all_tags)
        tags_dict[pdf_file] = tags
    #save dict to json
    
    json_file = os.path.join(data_dir, "tags.json")
    save_dict_to_json(tags_dict, json_file)
    
    