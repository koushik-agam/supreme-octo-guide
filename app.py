from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)


SANDBOX_URL = os.getenv("SANDBOX_URL")
SANDBOX_BASE_URL = os.getenv("SANDBOX_BASE_URL")
X_AUTH_TOKEN = os.getenv("X_AUTH_TOKEN")

spec = {"tags":["eSigning Gateway"]}

@app.route("/check_transaction_status", methods=["GET"])
@swag_from(spec)
def get_transaction_status():
    """
    Check the status of a transaction using the provided document ID.

    ---
    # tags:
    #   - eSigning Gateway
    parameters:
      - name: documentId
        in: query
        type: string
        required: true
        description: The document ID to check the transaction status.

    responses:
      200:
        description: Transaction status retrieved successfully.
        content:
          application/json:
            example:
              status: 1
              messages:
                - code: "200"
                  message: "Success"
              data:
                documentId: "123456"
                irn: "InternalRef123"
                folderId: "Folder123"
                requests:
                  - files: ["Base64EncodedFile1", "Base64EncodedFile2"]
                    auditTrail: "Base64EncodedAuditTrail"
                    signers:
                      - name: "Signer1Name"
                        pincode: "Signer1Pincode"
                        state: "Signer1State"
                        title: "Signer1Title"
                      - name: "Signer2Name"
                        pincode: "Signer2Pincode"
                        state: "Signer2State"
                        title: "Signer2Title"
      400:
        description: Bad Request.
        content:
          application/json:
            example:
              error: "Invalid request format"
      500:
        description: Failed to retrieve transaction status.
        content:
          application/json:
            example:
              error: "Failed to retrieve transaction status"
    """

    # Retrieve documentId from request parameters
    doc_id = request.args.get("documentId")

    # Check if documentId is provided
    if not doc_id:
        raise ValueError("documentId is required in the request parameters.")

    # Set request headers and parameters
    headers = {"X-Auth-Token": X_AUTH_TOKEN}
    parameters = {"documentId": doc_id}
    try:
        response = requests.get(url=f"{SANDBOX_URL}", params=parameters, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        result = response.json()
        # Check transaction status
        if result["status"] == 1:
            result["data"].pop("files", None)
            return result
        elif result["status"] == 0:
            return "Failed"
        else:
            return "Unknown Status"

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, timeouts)
        return f"Error: {str(e)}"


@app.route("/create_esigning_request", methods=["POST"])
@swag_from(spec)
def create_esigning_request():
    """
    Create a new esigning request
    
    ---
    # tags:
    #   - eSigning Gateway
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: The file to be uploaded and converted.
      - name: requestBody
        in: body
        required: true
        # description: Provide the ID of the Workflow from your Leegality Dashboard.
        schema:
          properties:
            profileId:
              type: string
              description: The first name of the user.
            name:
              type: string
              description: The last name of the user.
            file:
              type: string
              description: The date of birth of the user (YYYY-MM-DD).
    responses:
      200:
        description: Transaction status retrieved successfully.
        content:
          application/json:
            example:
              status: 1
              messages: []
              data:
                documentId: "FT803AA037"
                irn: "InternalRef123"
                invitees:
                  - active: true
                    email: "example@example.com"
                    expired: false
                    expiryDate: "05-01-2024 23:59:59"
                    name: "John Doe"
                    phone: "1234567890"
                    rejected: false
                    signType: "Digital"
                    signUrl: "https://sandbox.leegality.com/sign/73bca1a0-9bdd-4b5b-80ff-34d4a144e78b"
                    signed: false
      400:
        description: Bad Requestttt.
        content:
          application/json:
            example:
              error: "Invalid request format"
      500:
        description: Failed to retrieve transaction status.
        content:
          application/json:
            example:
              error: "Failed to retrieve transaction status"
    """
    data = request.get_json()

    # Check if required fields are present in the JSON request
    if "profileId" not in data or "name" not in data or "file" not in data:
        raise ValueError("Required fields (profileId, name, file) are missing in the JSON request.")
    print("After IF")
    image = request.files['image']  
    file_content = base64.b64encode(image.read())
    # Extract data from the JSON request
    profileId = data["profileId"]
    name = data["name"]
    print(f"image is {image}")
    print(f"name is {name}")
    print(f"profile id is {profileId}")
    print(f"file content is {file_content}")
    # file_content = data["file"]
    headers = {"X-Auth-Token": X_AUTH_TOKEN, "Content-Type": "application/json"}
    payload = {
        "profileId": profileId,
        "file": {
            "name": name,
            "file": file_content,
            "fields": [
                {
                    "id": "1569582963198",
                    "name": "Date of Agreement",
                    "type": "text",
                    "value": "30-12-2023",
                    "required": False
                },
                {
                    "id": "1569583138350",
                    "name": "Name of Borrower",
                    "type": "text",
                    "value": "Koushik",
                    "required": False
                },
                {
                    "id": "1569583161979",
                    "name": "PAN Number",
                    "type": "text",
                    "value": "XXXXX0000G",
                    "required": False
                },
                {
                    "id": "1569583192773",
                    "name": "Name of Parent",
                    "type": "text",
                    "value": "XYZ",
                    "required": False
                },
                {
                    "id": "1569583213364",
                    "name": "Address of Borrower",
                    "type": "text",
                    "value": "1/1 CBE",
                    "required": False
                },
                {
                    "id": "1569583239116",
                    "name": "Number of Months ",
                    "type": "text",
                    "value": "6",
                    "required": False
                },
                {
                    "id": "1569583266327",
                    "name": "Loan Amount",
                    "type": "text",
                    "value": "20000",
                    "required": False
                },
                {
                    "id": "1569583289700",
                    "name": "Loan Term",
                    "type": "text",
                    "value": "3",
                    "required": False
                }
            ]
        }
    }
    response = requests.post(url=SANDBOX_URL, headers=headers, json=payload)
    try:
        text = response.json()
        print("Type of text is ", type(text))
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {"error": f"Unable to parse response JSON: {str(e)}"}

        return jsonify(response_json), response.status_code
    except:
        return "Failed"

@app.route("/delete_document", methods=["DELETE"])
@swag_from(spec)
def delete_document():
    """
    Delete a document using its ID.

    ---
    # tags:
    #   - eSigning Gateway
    parameters:
      - name: documentId
        in: query
        type: string
        required: true
        description: The ID of the document to be deleted.

    responses:
      200:
        description: Document deleted successfully.
        content:
          application/json:
            example:
              status: 1
              messages: []
              data: {"message": "Document deleted successfully."}
      400:
        description: Bad Request.
        content:
          application/json:
            example:
              error: "Invalid request format"
      401:
        description: Unauthorized.
        content:
          application/json:
            example:
              error: "Unauthorized access"
      404:
        description: Document not found.
        content:
          application/json:
            example:
              error: "Document not found"
      500:
        description: Internal Server Error.
        content:
          application/json:
            example:
              error: "Failed to delete document"
    """
    document_id = request.args.get("documentId")
    headers = {"X-Auth-Token": X_AUTH_TOKEN}
    parameters = {"documentId": document_id}
    response = requests.delete(url=SANDBOX_URL, headers=headers, params=parameters)
    print(response.status_code)
    print(response.text)
    try:
        response_json = response.json()
    except Exception as e:
        response_json = {"error": f"Unable to parse response JSON: {str(e)}"}

    return jsonify(response_json), response.status_code


@app.route("/search", methods=["GET"])
@swag_from(spec)
def search():
    """
    Search for records based on a query.

    ---
    # tags:
    #   - eSigning Gateway
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: The search query.
      - name: status
        in: query
        type: string
        required: false
        description: The status to filter results (optional).
      - name: max
        in: query
        type: integer
        required: false
        default: 20
        description: The maximum number of records to retrieve (optional).

    responses:
      200:
        description: Search successful.
        content:
          application/json:
            example:
              status: 1
              messages: []
              data: {"result": "Success"}
      400:
        description: Bad Request.
        content:
          application/json:
            example:
              error: "Invalid request format"
      500:
        description: Internal Server Error.
        content:
          application/json:
            example:
              error: "Error: Internal Server Error"
    """
    # Get query parameters from the request
    query = request.args.get('q')

    # Check if the required 'q' parameter is present
    if not query:
        raise ValueError("The 'q' parameter is required in the request.")

    # Get optional parameters with default values
    status = request.args.get('status', None)
    max_records = request.args.get('max', 20, type=int)

    # Build the API URL with query parameters
    api_url = f"{SANDBOX_URL}/list?q={query}"

    if status is not None:
        api_url += f"&status={status}"

    api_url += f"&max={max_records}"

    # Set request headers
    headers = {"X-Auth-Token": X_AUTH_TOKEN}

    try:
        # Make API request
        response = requests.get(url=api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        # Process the response (optional)
        text = response.json()

        if text["status"] == 1:
            return "Success"
        elif text["status"] == 0:
            return "Failed"
        else:
            return "Unknown Status"

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500


@app.route("/reactivate_expired_documents", methods=["POST"])
@swag_from(spec)
def reactivate_expired_documents():
    """
    Reactivate expired documents.

    ---
    # tags:
    #   - eSigning Gateway
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            documentId:
              type: string
              description: The ID of the document to reactivate.

    responses:
      200:
        description: Document reactivation successful.
        content:
          application/json:
            example:
              result: "reactivate_expired_documents success"
      400:
        description: Bad Request.
        content:
          application/json:
            example:
              error: "Missing 'documentId' in the request body"
      500:
        description: Internal Server Error.
        content:
          application/json:
            example:
              error: "Error: Internal Server Error"
    """
    # Get JSON data from the request
    data = request.get_json()

    # Check if the required 'documentId' parameter is present
    if "documentId" not in data:
        return jsonify({"error": "Missing 'documentId' in the request body"}), 400

    document_id = data["documentId"]
    headers = {"X-Auth-Token": X_AUTH_TOKEN}
    json_data = {
        "documentId": document_id
    }

    try:
        # Make API request
        response = requests.post(url=SANDBOX_URL+"/reactivate", headers=headers, json=json_data)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        # Print response status code and content
        return "reactivate_expired_documents success"

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, timeouts)
        return jsonify({"error": f"Error: {str(e)}"}), 500


@app.route("/resend_notifications", methods=["POST"])
@swag_from(spec)
def resend_notifications():
    """
    Reactivate expired documents.

    ---
    # tags:
    #   - eSigning Gateway
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            documentId:
              type: string
              description: The ID of the document to reactivate.

    responses:
      200:
        description: Document reactivation successful.
        content:
          application/json:
            example:
              result: "reactivate_expired_documents success"
      400:
        description: Bad Request.
        content:
          application/json:
            example:
              error: "Missing 'documentId' in the request body"
      500:
        description: Internal Server Error.
        content:
          application/json:
            example:
              error: "Error: Internal Server Error"
    """
    data = request.get_json()

    if "signUrls" not in data or not isinstance(data["signUrls"], list):
        return jsonify({"error": "Invalid Data"}), 400

    sign_urls = data["signUrls"]
    headers = {"X-Auth-Token": X_AUTH_TOKEN}
    json_data = {"signUrls": sign_urls}
    response = requests.post(url=f"{SANDBOX_URL}/resend", headers=headers, json=json_data)

    try:
        response_json = response.json()
    except Exception as e:
        response_json = {"error": f"Unable to parse response JSON: {str(e)}"}

    return jsonify(response_json), response.status_code


@app.route("/delete_invitation", methods=["DELETE"])
@swag_from(spec)
def delete_invitation():
    """
    Delete an invitation.

    ---
    # tags:
    #   - eSigning Gateway
    parameters:
      - name: signUrl
        in: query
        type: string
        required: true
        description: The sign URL associated with the invitation.

    responses:
      200:
        description: Invitation deleted successfully.
        content:
          application/json:
            example:
              status: 1
              messages: []
              data: {}
      400:
        description: Bad Request.
        content:
          application/json:
            example:
              error: "Invalid request format"
      500:
        description: Internal Server Error.
        content:
          application/json:
            example:
              error: "Error: Internal Server Error"
    """
    sign_url = request.args.get('signUrl')
    DELETE_URL = SANDBOX_URL + "/invitation"
    headers = {"X-Auth-Token": X_AUTH_TOKEN}
    parameters = {
        "signUrl": sign_url
    }
    response = requests.delete(url=DELETE_URL, headers=headers, params=parameters)
    print(response.status_code)
    try:
        response_json = response.json()
    except Exception as e:
        response_json = {"error": f"Unable to parse response JSON: {str(e)}"}

    return jsonify(response_json), response.status_code


@app.route("/mark_complete", methods=["POST"])
@swag_from(spec)
def mark_complete():
    """
    Mark a document as complete.

    ---
    # tags:
    #   - eSigning Gateway
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            documentId:
              type: string
              description: The ID of the document to mark as complete.

    responses:
      200:
        description: Document marked as complete successfully.
        content:
          application/json:
            example:
              status: 1
              messages: []
              data: {}
      400:
        description: Bad Request.
        content:
          application/json:
            example:
              error: "Invalid request format"
      500:
        description: Internal Server Error.
        content:
          application/json:
            example:
              error: "Error: Internal Server Error"
    """
    data = request.get_json()

    json_data = {"documentId": data["documentId"]}
    headers = {"X-Auth-Token": X_AUTH_TOKEN}
    response = requests.post(url=f"{SANDBOX_URL}/complete", headers=headers, json=json_data)

    try:
        response_json = response.json()
    except Exception as e:
        response_json = {"error": f"Unable to parse response JSON: {str(e)}"}

    return jsonify(response_json), response.status_code


@app.route("/check_document", methods=["GET"])
@swag_from(spec)
def check_document():
    """
    Check details of a document.

    ---
    # tags:
    #   - eSigning Gateway
    parameters:
      - name: documentId
        in: query
        type: string
        required: true
        description: The ID of the document to check.

    responses:
      200:
        description: Document details retrieved successfully.
        content:
          application/json:
            example:
              status: 1
              messages: []
              data: {"documentId": "example_document_id", "status": "example_status"}
      400:
        description: Bad Request.
        content:
          application/json:
            example:
              error: "Invalid request format"
      404:
        description: Document not found.
        content:
          application/json:
            example:
              error: "Document not found"
      500:
        description: Internal Server Error.
        content:
          application/json:
            example:
              error: "Error: Internal Server Error"
    """
    document_id = request.args.get("documentId", None)

    headers = {"X-Auth-Token": X_AUTH_TOKEN}
    params = {"documentId": document_id}
    response = requests.get(url=f"{SANDBOX_URL}/document/details", headers=headers, params=params)

    try:
        response_json = response.json()
    except Exception as e:
        response_json = {"error": f"Unable to parse response JSON: {str(e)}"}

    return jsonify(response_json), response.status_code


@app.route("/check_list_of_completed_documents", methods=["GET"])
@swag_from(spec)
def check_list_of_completed_documents():
    """
    Check a list of completed documents.

    ---
    # tags:
    #   - eSigning Gateway
    parameters:
      - name: max
        in: query
        type: integer
        description: The maximum number of records to retrieve.
      - name: offset
        in: query
        type: integer
        description: The offset for paginating through records.
      - name: name
        in: query
        type: string
        description: The name associated with the completed documents.
      - name: irn
        in: query
        type: string
        description: The Internal Reference Number (IRN) associated with the completed documents.
      - name: folderId
        in: query
        type: string
        description: The folder ID associated with the completed documents.
      - name: startDate
        in: query
        type: string
        format: date
        description: The start date for filtering completed documents.
      - name: endDate
        in: query
        type: string
        format: date
        description: The end date for filtering completed documents.

    responses:
      200:
        description: List of completed documents retrieved successfully.
        content:
          application/json:
            example:
              status: 1
              messages: []
              data:
                - documentId: "example_document_id"
                  status: "completed"
                  name: "John Doe"
                  irn: "InternalRef123"
                  folderId: "example_folder_id"
                  completionDate: "2022-01-01"
                - documentId: "example_document_id_2"
                  status: "completed"
                  name: "Jane Doe"
                  irn: "InternalRef456"
                  folderId: "example_folder_id_2"
                  completionDate: "2022-01-02"
      400:
        description: Bad Request.
        content:
          application/json:
            example:
              error: "Invalid request format"
      500:
        description: Internal Server Error.
        content:
          application/json:
            example:
              error: "Error: Internal Server Error"
    """
    args = request.args
    headers = {"X-Auth-Token": X_AUTH_TOKEN}
    parameters = {
        "max": args.get("max"),
        "offset": args.get("offset"),
        "name": args.get("name"),
        "irn": args.get("irn"),
        "folderId": args.get("folderId"),
        "startDate": args.get("startDate"),
        "endDate": args.get("endDate")
    }
    response = requests.get(f"{SANDBOX_URL}/document/completed", headers=headers, params=parameters)

    try:
        response_json = response.json()
    except Exception as e:
        response_json = {"error": f"Unable to parse response JSON: {str(e)}"}

    return jsonify(response_json), response.status_code


@app.route("/esign_docsigner_invitation", methods=["POST"])
@swag_from(spec)
def esign_docsigner_invitation():
    """
    Send an invitation for eSign using DocSigner.

    ---
    # tags:
    #   - eSigning Gateway
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            signUrl:
              type: string
              description: The sign URL for the document.
            profileId:
              type: string
              description: The profile ID for the signing party.
            consent:
              type: boolean
              description: The consent status for the signing party.

    responses:
      200:
        description: Invitation sent successfully.
        content:
          application/json:
            example:
              status: 1
              messages: []
              data:
                documentId: "example_document_id"
                signUrl: "example_sign_url"
                profileId: "example_profile_id"
                consent: true
      400:
        description: Bad Request.
        content:
          application/json:
            example:
              error: "Invalid request format"
      500:
        description: Internal Server Error.
        content:
          application/json:
            example:
              error: "Error: Internal Server Error"
    """
    data = request.get_json()
    url = f"{SANDBOX_BASE_URL}/sign/docSigner/invitation"
    url = SANDBOX_BASE_URL + "/sign/docSigner/invitation"
    sign_url = data["signUrl"]
    profile_id = data["profileId"]
    consent = data["consent"]
    headers = {"Content-Type": "application/json", "X-Auth-Token": X_AUTH_TOKEN}
    json_data = {
        "signUrl": sign_url,
        "profileId": profile_id,
        "consent": consent
    }
    response = requests.post(url=url, headers=headers, json=json_data)

    try:
        response_json = response.json()
    except Exception as e:
        response_json = {"error": f"Unable to parse response JSON: {str(e)}"}

    return jsonify(response_json), response.status_code


if __name__ == "__main__":
    app.run(port=5555, debug=True)
