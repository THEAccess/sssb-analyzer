import csv

from disk import all_csv_files


def fix(directory: str):
    files = all_csv_files(directory)
    for file_path in files:
        p = directory + "/" + file_path
        with open(p, mode='r') as file:
            # reading the CSV file
            r = csv.reader(file)
            lines = list(r)
            if lines[0][0] != "Id":
                # displaying the contents of the CSV file
                with open(p, mode='w') as writefile:
                    w = csv.writer(writefile)

                    print("Fixing: " + file_path)
                    titles = ["Id", "Title", "Queue Days", "No. Applicants", "Moving in Date", "Floor", "Size (m²)",
                              "Rent (SEK)"]
                    lines.insert(0, titles)
                    w.writerows(lines)


if __name__ == '__main__':
    fix("/Users/yannickknoll/sssbscraper/2023-02-13_16-00-00")
