"""This is WifiRyu main module."""


from flask import Flask, jsonify, request
from preprocess import preprocessor
from utils import airodump_json_parser
from pathlib2 import Path
import os
import subprocess
import signal
import shlex


app = Flask(__name__)
monitor_interfaces = []


@app.route('/')
def home():
    print "Welcome to WiFiRyu!"


@app.route('/login')
def login():
    args = ""
    for i in request.args:
        args += args
    return str(args)


@app.route('/airmon/list')
def airmon_list():
    """Lists wireless interfaces present on machine.
    """
    output = (subprocess.check_output('airmon-ng').split('\n'))
    interfaces = []
    for line in output:
        if line != "" and line[0] != " ":
            print line.split("\t")
            if line.split("\t")[1] != "Interface":
                temp_dict = {}
                temp_dict['interface'] = line.split()[1]
                temp_dict['driver'] = line.split()[2]
                interfaces.append(temp_dict)
    print '[-] Interfaces = ' + str(interfaces)
    data = { 'status' : 'ok', 'interfaces':interfaces}
    resp = jsonify(data)
    resp.status_code = 200
    return resp


@app.route('/airmon/interface', methods=['PUT'])
def airmon_interface():
    """Start/stop monitor mode on an interface.
    """
    print request.args['operation'] + ' ' + request.args['interface']
    output = subprocess.check_output(['airmon-ng ' +
                                      request.args['operation'] +
                                      ' ' +
                                      request.args['interface']],
                                     shell=True)
    if request.args['operation'].lower() == 'start':
        output = output.split('mac80211 monitor mode vif enabled')[1] \
            .split('\n')[0].split(' on ')[1].split(']')[1][:-1]
        if not monitor_interfaces.__contains__(output):
            monitor_interfaces.append(output)
    else:
        output = output.split('mac80211 station mode vif enabled')[1] \
            .split('\n')[0].split(' on ')[1].split(']')[1][:-1]
        if monitor_interfaces.__contains__(output):
            monitor_interfaces.remove(output)
    data = {}
    data['status'] = 'ok'
    data['interface'] = output
    resp = jsonify(data)
    resp.status_code = 200
    return resp


@app.route('/airmon/check')
def airmon_check():
    """Returns a list of all possible programs
    that could interfere with monitor card.
    """
    output = subprocess.check_output(['airmon-ng check'], shell=True)
    processes = []
    if output.__contains__('PID Name'):
        output = output.split('PID Name')[1].split('\n')
        for process in output:
            if process != '':
                processes.append(process.strip().split(' ')[1])
        print processes
    data = {}
    data['status'] = 'ok'
    data['processes'] = processes
    resp = jsonify(data)
    resp.status_code = 200
    return resp


@app.route('/airmon/checkkill')
def airmon_checkkill():
    """Try to kill all possible programs
    that could interfere with monitor card.
    """
    output = subprocess.check_output(['airmon-ng check kill'], shell=True)
    processes = []
    if output.__contains__('PID Name'):
        output = output.split('PID Name')[1].split('\n')
        for process in output:
            if process != '':
                processes.append(process.strip().split(' ')[1])
        print processes
    data = {}
    data['status'] = 'ok'
    data['processes'] = processes
    resp = jsonify(data)
    resp.status_code = 200
    return resp


@app.route('/airmon/moninterface', methods=['GET'])
def airmon_moninterface():
    """List all monitor mode interfaces.
    """
    data = {}
    data['status'] = 'ok'
    data['interfaces'] = monitor_interfaces
    resp = jsonify(data)
    resp.status_code = 200
    return resp


@app.route('/airodump', methods=['GET'])
def airodump():
    """Returns airodump-ng output.
    """
    dump_file = Path('/tmp/ryu/airodump-sample.csv')
    if dump_file.is_file():
        return airodump_json_parser('/tmp/ryu/airodump-sample.csv')
    else:
        data = {}
        data['status'] = 'error'
        data['message'] = 'Airodump output file not found.'
        resp = jsonify(data)
        resp.status_code = 200
        return resp


@app.route('/airodump', methods=['PUT'])
def airodump_op():
    """Start/stop airodump-ng with different arguments.
    """
    cmd = 'airodump-ng '
    request_data = request.get_json()
    operation = request_data['operation']
    if operation.lower() == 'start':
        if request_data['attributes']['gpsd'] == "True":
            cmd += '--gpsd '
        if request_data['attributes']['berlin'] != 0:
            cmd += '--berlin ' + \
                   str(request_data['attributes']['berlin']) + ' '
        if request_data['attributes']['band'] != "":
            cmd += '--band ' + \
                str(request_data['attributes']['band']) + ' '

        if request_data['attributes']['manufacturer'] == "True":
            cmd += '--manufacturer '
        if request_data['attributes']['uptime'] == "True":
            cmd += '--uptime '
        if request_data['attributes']['wps'] == "True":
            cmd += '--wps '
        if request_data['attributes']['write-interval'] != 0:
            cmd += '--write-interval ' + \
                   str(request_data['attributes']['write-interval']) + ' '
        if request_data['attributes']['encrypt'] != "":
            cmd += '--encrypt ' + \
                   str(request_data['attributes']['encrypt']) + ' '
        if request_data['attributes']['bssid'] != "":
            cmd += '--bssid ' + \
                   str(request_data['attributes']['bssid']) + ' '
        if request_data['attributes']['essid-regex'] != "":
            cmd += '--essid-regex ' + \
                   str(request_data['attributes']['essid-regex']) + ' '
        cmd += '-w /tmp/ryu/airodump '
        interface = request_data['interface']
        cmd += interface
        print 'cmd = ' + cmd
        proc = subprocess.Popen(shlex.split(cmd))
        data = {}
        data['status'] = 'ok'
        data['pid'] = proc.pid
        resp = jsonify(data)
        resp.status_code = 200
        return resp
    else:
        os.kill(request_data['pid'], signal.SIGKILL)
        data = {}
        data['status'] = 'ok'
        data['pid'] = -1
        resp = jsonify(data)
        resp.status_code = 200
        return resp


@app.errorhandler(404)
def not_found(error=None):
    data = { 'status': 'error',
             'message': 'Not found; ' + request.url,
             }
    resp = jsonify(data)
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    preproc = preprocessor()
    preproc.prepare_output_dir()
    app.run(debug=True)
