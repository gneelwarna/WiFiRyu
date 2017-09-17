def get_header(header):
    header = header.strip('\n').strip('\r').rsplit(',')
    striped_header = []
    for i in header:
        striped_header.append(str(i).strip(' '))
    return striped_header


def get_entry(entry):
    entry = entry.strip('\n').strip('\r').rsplit(',')
    striped_entry = []
    for i in entry:
        striped_entry.append(str(i).strip(' '))
    return striped_entry


def airodump_parser(airodump_file):
    f = open(airodump_file, 'r')
    f.readline() # Blank line

    header = get_header(f.readline())
    entries = []
    while True:
        line = f.readline()
        if line in ['\n', '\r\n']:
            break
        line = get_entry(line)
        entries.append(line)
    return header, entries


'''
if __name__ == '__main__':
    header, entries = airodump_parser('/root/1-01.csv')
    print header
    print entries
'''
