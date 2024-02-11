from flask import Flask, request, render_template_string
import base64
import google.cloud.dlp
import os
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound

app = Flask(__name__)

def access_secret_version(project_id, secret_id, version_id="latest"):
    """
    Access a secret version in Google Cloud Secret Manager.

    Args:
    project_id: GCP project ID
    secret_id: ID of the secret to access
    version_id: Version of the secret (default is "latest")

    Returns:
    The payload of the secret version as a string.
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        # Access the secret version.
        response = client.access_secret_version(request={"name": name})

        # Return the payload as a string.
        return response.payload.data.decode("UTF-8")
    except NotFound:
    
        print(f"Secret with ID '{secret_id}' not found.")
        return None
        
project_input = os.getenv('project_name','') #feting from environment variable
surrogate_input = os.getenv('surrogate_name','') #feting from environment variable
secret_id_key="key_name" 
key_name = access_secret_version(project_input, secret_id_key) #fetching from secret manager
secret_id_wrap="wrapkey_name"
wrapkey_name = access_secret_version(project_input, secret_id_wrap) #fetching from secret manager

@app.route('/', methods=['GET', 'POST'])
def home():
    global project_input,surrogate_input,key_name,wrapkey_name
    message = ''
    if request.method == 'POST':
        encrypted_input = request.form['encrypted_input']
        decrypted = reidentify_with_deterministic(project_input,encrypted_input,surrogate_input,key_name,wrapkey_name)
        message = f'{decrypted}'
    return render_template_string('''
        <html>
            <body>
                <form method="post">
                    Enter the data to Re-Identify:<br><br>
                    <textarea id="w3review" name="encrypted_input" rows="10" cols="50">Sample JSON with sensitive data goes here</textarea><br><br>
                    <input type="submit" value="Submit"/>
                </form>
                <pre><code>
                <p>{{ message }}</p>
                </code></pre>
            </body>
        </html>
    ''', message=message)
    
def reidentify_with_deterministic(
    project: str,
    input_str: str,
    surrogate_type: str = None,
    key_name: str = None,
    wrapped_key: str = None,
) -> None:
    """Re-identifies content that was previously de-identified through deterministic encryption.
    Args:
        project: The Google Cloud project ID to use as a parent resource.
        input_str: The string to be re-identified. Provide the entire token. Example:
            EMAIL_ADDRESS_TOKEN(52):AVAx2eIEnIQP5jbNEr2j9wLOAd5m4kpSBR/0jjjGdAOmryzZbE/q
        surrogate_type: The name of the surrogate custom infoType used
            during the encryption process.
        key_name: The name of the Cloud KMS key used to encrypt ("wrap") the
            AES-256 key. Example:
            keyName = 'projects/YOUR_GCLOUD_PROJECT/locations/YOUR_LOCATION/
            keyRings/YOUR_KEYRING_NAME/cryptoKeys/YOUR_KEY_NAME'
        wrapped_key: The encrypted ("wrapped") AES-256 key previously used to encrypt the content.
            This key must have been encrypted using the Cloud KMS key specified by key_name.
    Returns:
        None; the response from the API is printed to the terminal.
    """
    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # The wrapped key is base64-encoded, but the library expects a binary
    # string, so decode it here.
    wrapped_key = base64.b64decode(wrapped_key)

    # Construct reidentify Configuration
    reidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "primitive_transformation": {
                        "crypto_deterministic_config": {
                            "crypto_key": {
                                "kms_wrapped": {
                                    "wrapped_key": wrapped_key,
                                    "crypto_key_name": key_name,
                                }
                            },
                            "surrogate_info_type": {"name": surrogate_type},
                        }
                    }
                }
            ]
        }
    }

    inspect_config = {
        "custom_info_types": [
            {"info_type": {"name": surrogate_type}, "surrogate_type": {}}
        ]
    }

    # Convert string to item
    item = {"value": input_str}
    
    stored_info_type_name = "projects/pseudo-dlp-demo2/locations/global/inspectTemplates/CVV_Check"
    # Call the API
    response = dlp.reidentify_content(
        request={
            "parent": parent,
            "reidentify_config": reidentify_config,
            "inspect_config": inspect_config,
            "inspect_template_name":stored_info_type_name,
            "item": item,
        }
    )

    # Print results
    print(response.item.value)
    decrypted = response.item.value
    return decrypted

    


if __name__ == '__main__':
    app.run(debug=True)
