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


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_or_create_survey_photos_folder(drive, parent_folder_id):
    """Find or create a 'Survey Photos' folder inside the parent folder."""
    try:
        file_list = drive.ListFile({
            'q': f"'{parent_folder_id}' in parents and title='Survey Photos' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        }).GetList()
        
        if file_list:
            survey_folder_id = file_list[0]['id']
            logger.info(f"Found existing 'Survey Photos' folder with ID: {survey_folder_id}")
            return survey_folder_id
        else:
            logger.info("'Survey Photos' folder not found, creating new one...")
            survey_folder = drive.CreateFile({
                'title': 'Survey Photos',
                'parents': [{'id': parent_folder_id}],
                'mimeType': 'application/vnd.google-apps.folder'
            })
            survey_folder.Upload()
            survey_folder_id = survey_folder['id']
            logger.info(f"Created new 'Survey Photos' folder with ID: {survey_folder_id}")
            return survey_folder_id
            
    except Exception as e:
        logger.error(f"Error finding or creating 'Survey Photos' folder: {e}")
        raise


def upload_image_to_drive(image_path, folder_id, recipient_email=None, is_client=False):
    """Faz upload de uma imagem para o Google Drive."""
    import os

    try:
        drive = get_drive_service()

        if is_client:
            final_folder_id = os.environ.get('DRIVE_CLIENTS_FOLDER')
        else:
            final_folder_id = find_or_create_survey_photos_folder(drive, folder_id)

        file_name = os.path.basename(image_path)
        gdrive_file = drive.CreateFile({
            'title': file_name, 
            'parents': [{'id': final_folder_id}]
        })
        gdrive_file.SetContentFile(image_path)
        gdrive_file.Upload()

        image_url = None
        try:
            permission = {}

            # Wait for file to be properly uploaded before setting permissions
            gdrive_file.FetchMetadata()
            
            if recipient_email:
                permission = {
                    'type': 'user', 
                    'role': 'reader', 
                    'value': recipient_email,
                    'sendNotificationEmails': False  # Avoid sending emails
                }
            else:
                permission = {
                    'type': 'anyone', 
                    'role': 'reader'
                }
            
            # Add error handling for permission insertion
            result = gdrive_file.InsertPermission(permission)
            logger.info(f"Permission set successfully: {result}")

            if 'id' in gdrive_file:
                image_url = f"https://drive.google.com/thumbnail?id={gdrive_file['id']}"
                
        except Exception as e_perm:
            logger.warning(f"Erro ao definir permissão: {e_perm}")

        return image_url

    except Exception as e:
        logger.error(f"Erro ao autenticar ou fazer upload: {e}")
        return None


def delete_file_from_drive(file_id):
    """Deleta um arquivo do Google Drive pelo ID."""
    try:
        drive = get_drive_service()
        file_to_delete = drive.CreateFile({'id': file_id})
        file_to_delete.Trash()
        return True
    except Exception as e:
        logger.error(f"Erro ao deletar arquivo do Google Drive: {e}")
        return False