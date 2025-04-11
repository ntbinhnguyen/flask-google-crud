import os
import tempfile
from googleapiclient.discovery import build
from google.oauth2 import service_account
from sheets import get_all_data

SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
docs_service = build('docs', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

TEMPLATE_ID = os.getenv("DOC_TEMPLATE_ID")

def generate_doc_and_export_pdf(index):
    row = get_all_data()[index]
    doc = docs_service.documents().copy(body={"name": f"Report_{row['Name']}"}, documentId=TEMPLATE_ID).execute()
    doc_id = doc['documentId']
    requests = [
        {"replaceAllText": {"containsText": {"text": "{{name}}", "matchCase": True}, "replaceText": row["Name"]}},
        {"replaceAllText": {"containsText": {"text": "{{email}}", "matchCase": True}, "replaceText": row["Email"]}},
        {"replaceAllText": {"containsText": {"text": "{{note}}", "matchCase": True}, "replaceText": row["Note"]}},
    ]
    docs_service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_content = drive_service.files().export(fileId=doc_id, mimeType='application/pdf').execute()
    with open(pdf_file.name, 'wb') as f:
        f.write(pdf_content)
    return pdf_file.name