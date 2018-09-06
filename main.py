import zipfile as zip
import yaml as yml
import os
import subprocess
import http.server as simple_http
import socketserver as sock

# Load the config file
config_file = open("./config.yaml","r").read()
config = yml.load(config_file)

zip_config = config['zips']
server_config = config['server']
port = 3000

# Set port
if server_config['port']:
    port = server_config['port']
else:
    print("Port not specified. Using default.")

# Helpers
def make_abs_path(path):
    if path.startsWith('/'):
        return path
    else:
        return '/' + path

def app_dir(dir,path):
    return dir + '/' + path 

def mk_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

output_path = "./out"
mk_dir(output_path)

def mk_archive(spec):
    archive_name = app_dir(output_path,spec['alias']) + ".zip"
    print("Creating archive: " + archive_name)
    level = 7
    if spec['compression-level']:
        level = spec['compression-level']
    return zip.ZipFile(archive_name, "w", zip.ZIP_DEFLATED, level)

def zip_em(conf):
    for key, val in conf.items():
        print("Running zip task: " + key)
        archive = mk_archive(val)
        input_dir = val['input-dir']
        for f in os.listdir(input_dir):
            file_dir = app_dir(input_dir, f)
            print("Writing \"" + f + "\" to archive...")
            archive.write(filename=file_dir,arcname=f)

# Make the archives
zip_em(zip_config)

# Serve 'em up
def serve_em(conf):
    handler = simple_http.SimpleHTTPRequestHandler
    httpd = sock.TCPServer(("", port), handler)

    print("Serving zips at port: " + str(port))
    httpd.serve_forever()