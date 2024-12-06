import os
import uuid
from werkzeug.utils import secure_filename
from pathlib import Path


class UploadFileService:

    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "xlsx", "xls", "docx", "doc"}
    BASE_DIR = Path(__file__).resolve().parent.parent
    FOLDER_PATH = f"{BASE_DIR}/static/{UPLOAD_FOLDER}"

    def __init__(self):
        """Khởi tạo service upload file"""
        self.initFolderUpload()

    def initFolderUpload(self):
        # Nếu không tồn tại thực hiện tạo folder mới
        if not os.path.exists(self.FOLDER_PATH):
            os.makedirs(self.FOLDER_PATH)

    def is_allowed_file(self, filename):
        """
        Kiểm tra tệp có đúng định dạng cho phép hay không.
        """
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in self.ALLOWED_EXTENSIONS
        )

    def saveToMultipleFile(self, files):
        saved_files = []
        error_files = []

        for file in files:
            if file:
                if self.is_allowed_file(file.filename):
                    # Xử lý tên file để tránh lỗi hoặc tấn công
                    file_extension = os.path.splitext(file.filename)
                    file_name = f"{str(uuid.uuid4())}{file_extension[1]}"
                    save_path = os.path.join(self.FOLDER_PATH, file_name)
                    # Lưu file vào thư mục
                    file.save(save_path)
                    saved_files.append(
                        {
                            "id": str(uuid.uuid4()),
                            "file_name": secure_filename(file.filename),
                            "file_url": f"static/{self.UPLOAD_FOLDER}/{file_name}",
                            "file_type": file.content_type,
                            "file_size": os.path.getsize(save_path),
                        }
                    )
                else:
                    error_files.append(file.filename)

        return saved_files, error_files

    def removeMultipleFileByIds(self, fileIds):
        pass
