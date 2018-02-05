"""This is utils module. It creates JSON
out of airodump-ng csv output file."""


from flask import jsonify


def strip_input(entry):
    entry = entry.strip('\n').strip('\r').rsplit(',')
    stripped_entry = []
    for i in entry:
        stripped_entry.append(str(i).strip(' '))
    return stripped_entry


def airodump_json_parser(airodump_file):
    f = open(airodump_file, 'r')
    f.readline() # Blank line

    header = strip_input(f.readline())
    json_array = []
    while True:
        json_entry = {}
        line = f.readline()
        if line in ['\n', '\r\n']:
            break
        header_list = map(str, header)
        line_list = map(str, strip_input(line))
        entry_item = iter(line_list)
        for header_item in header_list:
            json_entry[header_item] = str(entry_item.next())
        json_array.append(json_entry)
    return jsonify(json_array)
