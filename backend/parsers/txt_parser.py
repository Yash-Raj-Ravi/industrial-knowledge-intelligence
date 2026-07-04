def parse_txt(file_path: str) -> str:
    with open (file_path,"r", encoding="utf-8") as file: # encoding="utf-8" correctly handles most text files.
        return file.read().strip() # read() reads the entire file as a single string