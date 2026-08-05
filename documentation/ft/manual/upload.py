import os
import sys
import requests
import urllib.parse
import zipfile

# Get the target environment from command-line arguments
target_env = sys.argv[1] if len(sys.argv) > 1 else 'prod'

# Define the variables
zip_archive = 'ai_sdk_manual.zip'  # Path where the new ZIP file will be saved
file_to_zip = 'mkdocs.yml'  # File to include in the ZIP
folder_to_zip = 'Manual/'  # Folder to include in the ZIP

# Set the API key and base URL based on the target environment
if target_env == 'staging':
    api_key = os.getenv('FT_Pub')
    url_base = 'https://siemens-fa-staging.fluidtopics.net'
else:
    api_key = os.getenv('FT_Pub_prod')
    url_base = 'https://siemens-fa.fluidtopics.net'

source_id = 'MKDOCS'  # Replace with your actual source ID
publisher = os.getenv('GITLAB_USER_LOGIN')
user_email = os.getenv('GITLAB_USER_EMAIL')

# Validate GitLab user login and email
if not publisher or not user_email:
    raise ValueError("GitLab user login or email is not set in the environment variables.")
    
# URL-encode the publisher variable
encoded_publisher = urllib.parse.quote(publisher, safe='')  # URL-encode the publisher for the API request

# Create a ZIP file containing the specified file and folder
with zipfile.ZipFile(zip_archive, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Add file
    zipf.write(file_to_zip, os.path.basename(file_to_zip))
    # Add folder with renamed path to "docs"
    for root, dirs, files in os.walk(folder_to_zip):
        for file in files:
            file_path = os.path.join(root, file)
            # Replace the folder name with "docs" in the archive
            arcname = os.path.join('docs', os.path.relpath(file_path, folder_to_zip))
            zipf.write(file_path, arcname)

# Define the URL
endpoint_post = f'/api/admin/khub/sources/{source_id}/upload'
url = url_base + endpoint_post

# Define the headers
headers = {
    'Authorization': f'Bearer {api_key}'
}

# Define the payload
payload = {}

# Log the URL and headers for debugging
print(f"URL: {url}")
print(f"Headers: {headers}")

# Send the POST request
with open(zip_archive, 'rb') as f:
    files = {'file': (zip_archive, f, 'application/zip')}
    response = requests.post(url, headers=headers, data=payload, files=files)
    
# Print the response status code and content
print(response.status_code)
print(response.text)