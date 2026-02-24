import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_drive_service():
    import os
    from pydrive2.drive import GoogleDrive
    from pydrive2.auth import GoogleAuth
    from pydrive2.auth import ServiceAccountCredentials
    
    """Autentica e retorna o serviço do Google Drive usando Service Account."""
    credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if not credentials_json:
        logger.warning("GOOGLE_APPLICATION_CREDENTIALS_JSON not set")
        raise Exception("Missing Google credentials")

    credentials_dict = json.loads(credentials_json)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        credentials_dict,
        scopes=['https://www.googleapis.com/auth/drive']
    )

    gauth = GoogleAuth()
    gauth.auth_method = 'service'
    gauth.credentials = credentials
    drive = GoogleDrive(gauth)
    return drive

def find_or_create_invoice_folder(drive, parent_folder_id):
    """Find or create a 'Nota Fiscal' folder inside the parent folder."""
    try:
        file_list = drive.ListFile({
            'q': f"'{parent_folder_id}' in parents and title='Nota Fiscal' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        }).GetList()
        
        if file_list:
            invoice_folder_id = file_list[0]['id']
            logger.info(f"Found existing 'Nota Fiscal' folder with ID: {invoice_folder_id}")
            return invoice_folder_id
        else:
            logger.info("'Nota Fiscal' folder not found, creating new one...")
            invoice_folder = drive.CreateFile({
                'title': 'Nota Fiscal',
                'parents': [{'id': parent_folder_id}],
                'mimeType': 'application/vnd.google-apps.folder'
            })
            invoice_folder.Upload()
            invoice_folder_id = invoice_folder['id']
            logger.info(f"Created new 'Nota Fiscal' folder with ID: {invoice_folder_id}")
            return invoice_folder_id
            
    except Exception as e:
        logger.error(f"Error finding or creating 'Nota Fiscal' folder: {e}")
        raise

def find_or_create_survey_reports_folder(drive, parent_folder_id):
    """Find or create a 'Survey Reports' folder inside the parent folder."""
    try:
        file_list = drive.ListFile({
            'q': f"'{parent_folder_id}' in parents and title='Survey Reports' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        }).GetList()
        
        if file_list:
            survey_folder_id = file_list[0]['id']
            logger.info(f"Found existing 'Survey Reports' folder with ID: {survey_folder_id}")
            return survey_folder_id
        else:
            logger.info("'Survey Reports' folder not found, creating new one...")
            survey_folder = drive.CreateFile({
                'title': 'Survey Reports',
                'parents': [{'id': parent_folder_id}],
                'mimeType': 'application/vnd.google-apps.folder'
            })
            survey_folder.Upload()
            survey_folder_id = survey_folder['id']
            logger.info(f"Created new 'Survey Reports' folder with ID: {survey_folder_id}")
            return survey_folder_id
            
    except Exception as e:
        logger.error(f"Error finding or creating 'Survey Reports' folder: {e}")
        raise


def upload_report_to_drive(file_path, folder_id):
    """Faz upload de uma imagem para o Google Drive."""
    import os

    try:
        drive = get_drive_service()

        final_folder_id = find_or_create_survey_reports_folder(drive, folder_id)

        file_name = os.path.basename(file_path)
        gdrive_file = drive.CreateFile({
            'title': file_name, 
            'parents': [{'id': final_folder_id}]
        })
        gdrive_file.SetContentFile(file_path)
        gdrive_file.Upload()

        file_url = None
        try:

            gdrive_file.InsertPermission({'type': 'anyone', 'role': 'reader'})

            if 'id' in gdrive_file:
                file_url = f"https://drive.google.com/uc?id={gdrive_file['id']}&export=download"
        except Exception as e_perm:
            logger.warning(f"Erro ao definir permissão: {e_perm}")

        return file_url

    except Exception as e:
        logger.error(f"Erro ao autenticar ou fazer upload: {e}")
        return None


def upload_invoice_to_drive(file_path, folder_id):
    """Upload de nota fiscal PDF para o Google Drive."""
    import os

    try:
        drive = get_drive_service()

        final_folder_id = find_or_create_invoice_folder(drive, folder_id)

        file_name = os.path.basename(file_path)
        gdrive_file = drive.CreateFile({
            'title': file_name, 
            'parents': [{'id': final_folder_id}]
        })
        gdrive_file.SetContentFile(file_path)
        gdrive_file.Upload()

        file_url = None
        try:
            gdrive_file.InsertPermission({'type': 'anyone', 'role': 'reader'})

            if 'id' in gdrive_file:
                file_url = f"https://drive.google.com/uc?id={gdrive_file['id']}&export=download"
        except Exception as e_perm:
            logger.warning(f"Erro ao definir permissão: {e_perm}")

        return file_url

    except Exception as e:
        logger.error(f"Erro ao autenticar ou fazer upload: {e}")
        return None