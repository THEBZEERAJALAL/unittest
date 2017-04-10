import json
import csv
import sys
def to_string(s):
    try:
        return str(s)
    except:
        return s.encode('utf-8')

def reduce_item(key, value):
    global reduced_item

    if type(value) is list:
            reduce_item(key + "_start", value[0])
            reduce_item(key + "_end", value[-1])

    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:

            if type(value[sub_key]) is dict:
                StrDict = to_string(sub_key)

                if (StrDict == "train_meta"):
                    reduce_item(to_string(sub_key), value[sub_key])
                else:
                    continue
            else:
                reduce_item(to_string(sub_key), value[sub_key])
    else:
        reduced_item[to_string(key)] = to_string(value)
if __name__ == "__main__":

    json_file_path = "/home/thebzeera/PycharmProjects/new/sample.json"
    csv_file_path = "/home/thebzeera/PycharmProjects/new/sample.csv"

    fp = open(json_file_path, 'r')
    json_value = fp.read()
    raw_data = json.loads(json_value)
    processed_data = []
    header = []
    header.append("ID")
    reduced_item = {}
    for p in range(0,13):
        node = to_string(p)
        try:
            data_to_be_processed = raw_data[node]
        except:
            data_to_be_processed = raw_data
        reduce_item(node, data_to_be_processed)
        header += reduced_item.keys()
        stringP=to_string(p)
        reduced_item["ID"]=stringP
        processed_data.append(reduced_item.copy())
        header = list(set(header))
        header.sort()
    with open(csv_file_path, 'w') as f:
        writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in processed_data:
            writer.writerow(row)

    print("Just completed writing csv file with %d columns" % len(header))