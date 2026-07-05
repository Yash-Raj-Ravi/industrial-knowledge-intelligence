UPLOAD_DIR = "uploads"

ALLOWED_TYPES = {"application/pdf",

                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # DOCX

                 "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # PPTX

                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # XLSX

                 "text/plain",

                 "text/csv",

                 "image/png",

                 "image/jpeg"
                 }
# Chunking 
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


