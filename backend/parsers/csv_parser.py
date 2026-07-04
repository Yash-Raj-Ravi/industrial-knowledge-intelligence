import csv

def parse_csv(file_path: str) -> str:
    lines = [] # # List to store the text representation of each row by joining about comma
    with open(file_path,"r",encoding="utf-8") as file:
        reader = csv.reader(file) # It reads the csv file row wise and stores them with comma separation for each column
        for row in reader:
            lines.append(",".join(row))
        return "\n".join(lines).strip()