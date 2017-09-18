from flask import Flask
from preprocessor import preprocessor
from parser import airodump_parser


app = Flask(__name__)


@app.route('/', methods=['get'])
def home():
    #Read airodump-ng output csv file.
    header, entries = airodump_parser('/root/1-01.csv')
    return 'Welcome to WiFiRyu!' + str(header) + ' - ' + str(entries)


def main():
    print 'Welcome to WiFiRyu -->'
    # Prepare output directory in /tmp to for airodump-ng
    preprocessor().prepare_output_dir()
    #Create monitor mode interface.
    #Code to be added.

    #Start airodump-ng in subprocess.
    #Code to be added.

    #Read airodump-ng output csv file.
    #header, entries = airodump_parser('/root/1-01.csv')


if __name__ == '__main__':
    app.run(debug=True)
    main()
