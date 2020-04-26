import os
import csv


def get_image_id_count(imageid):
    count = 0
    for file in os.listdir("images/"):
        if file.startswith(imageid):
            count += 1
    return count


if __name__ == "__main__":
    data = []
    images = os.listdir("images/")
    for file in os.listdir("data/"):
        with open("data/" + file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.keys().__contains__("imageIdCount"):
                    data.append(row)
                else:
                    row["imageIdCount"] = get_image_id_count(row["imageId"])
                    data.append(row)

    with open("data_combined.csv", 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)