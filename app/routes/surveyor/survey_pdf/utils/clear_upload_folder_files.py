import os

def clear_upload_folder_files():
    folder = os.path.join(os.getcwd(), 'uploads')

    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Erro ao deletar arquivo {file_path}: {e}")