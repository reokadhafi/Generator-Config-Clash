# %%
import random
import string
import json
import yaml
from urllib.parse import urlparse, parse_qs
from base64 import b64decode

# pembuat string random
def generate_random_string(length):
    characters = string.digits + string.ascii_lowercase
    return ''.join(random.choice(characters) for _ in range(length))

# kumpulan parser terpakai di function add_akun


def parser_trojan(data):
    parsed_url = urlparse("trojan://"+data)
    query_params = parse_qs(parsed_url.query)
    if parsed_url.scheme != "trojan" or not parsed_url.netloc:
        print("Data akun Trojan tidak valid!")
        return
    password = parsed_url.netloc.split("@")[0]
    server = parsed_url.netloc.split("@")[1].split(":")[0]
    port = parsed_url.port
    sni = query_params.get("sni", [""])[0]
    tipe = query_params.get("type", [""])[0]
    host = query_params.get("host", [""])[0]
    path = query_params.get("path", [""])[0]
    data_dict = {
        "password": password,
        "server": server,
        "port": port,
        "sni": sni,
        "type": tipe,
        "host": host,
        "path": path
    }
    if tipe == "":
        for i in data_dict:
            data_dict[i] = None
    if tipe == "grpc":
    	servicename = query_params.get("serviceName", [""])[0]
    	data_dict["network"] = "grpc"
    	data_dict["grpc-service-name"] = servicename
    return data_dict


def parser_v2ray(data):
    dd = b64decode(data + '=' * (-len(data) % 4)).decode()
    rl = (dd.replace(" ", "").replace("\r", "").replace(
        "\n", "")).replace('"', "'")[1:-1].replace("GET-:wss://", "formatbaru//").replace("http://", "http=//")
    db1 = {
        'add': '',
        'aid': '',
        'host': '',
        'id': '',
        'net': '',
        'path': '',
        'port': '',
        'ps': '',
        'scy': '',
        'sni': '',
        'tls': '',
        'type': '',
        'v': ''
    }
    for i in range(len(rl.split(':'))-1):
        dt = rl.split(",")[i].replace("'", '').split(":")
        db1[dt[0]] = dt[1]
        #print(dt)
    return db1


def parser_ss(data):
    db1 = {
        'password': '',
        'server': '',
        'port': '80',
        'udp-over-tcp': 'true',
        'plugin': 'v2ray-plugin',
        'path': '',
    }
    rl = (data.replace(" ", "").replace(
        "/", "").replace("%2F", "/").replace("%3B", "&").replace("%3D", "=").replace("#", "&name="))
    dd = b64decode(rl.split("@")[0] + '=' *
                   (-len(rl.split("@")[0]) % 4)).decode()
    db1['password'] = dd.split(":")[1]
    db1['cipher'] = dd.split(":")[0]
    db1['server'] = rl.split('@')[1].split(':')[0]
    dt = rl.split('?')[1].split("&")
    for i in range(len(dt)):
        dt2 = dt[i].split("=")
        db1[dt2[0]] = dt2[1]
    return db1

# menulis ke file database


def write_database(add_or_clear_akun, filename="log.json"):
    with open(filename, "w") as db:
        json.dump(add_or_clear_akun, db)


def add_akun(string_akun):
    with open("log.json") as json_files:
        data = json.load(json_files)
        akun_mentah = data["akun_mentah"]
        akun_parsing = data["akun_parsing"]
        db = {}
        if string_akun[0:8] == 'vmess://':
            db = string_akun.replace('vmess://', '')
            akun_mentah["vmess"].append(db)
            akun_parsing["vmess"].append(
                parser_v2ray(db))
        elif string_akun[0:8] == 'trojan:/':
            db = string_akun.replace('trojan://', '')
            akun_mentah["trojan"].append(db)
            akun_parsing["trojan"].append(parser_trojan(db))
        elif string_akun[0:8] == 'trojan-g':
            db = string_akun.replace('trojan-go://', '')
            akun_mentah["trojan"].append(db)
            akun_parsing["trojan"].append(parser_trojan(db))
        elif string_akun[0:5] == 'ss://':
            db = string_akun.replace('ss://', '')
            akun_mentah["ss"].append(db)
            akun_parsing["ss"].append(parser_trojan(db))
        return data

# untuk menghapus data akun sesuai jenis (vmess,trojan,ss)


def clear_akun(jenis_akun):
    with open("log.json") as json_files:
        data = json.load(json_files)
        akun_mentah = data["akun_mentah"]
        akun_parsing = data["akun_parsing"]
    if jenis_akun == "vmess":
        akun_mentah["vmess"].clear()
        akun_parsing["vmess"].clear()
    if jenis_akun == "trojan":
        akun_mentah["trojan"].clear()
        akun_parsing["trojan"].clear()
    if jenis_akun == "ss":
        akun_mentah["ss"].clear()
        akun_parsing["ss"].clear()
    return data
# write_database(add_akun(data))
# write_database(clear_akun("vmess"))

# %%
# mencari nama server sesuai data server


def nama_server(server):
    with open("db_server.json") as json_file:
        data = json.load(json_file)
    for i, bc in data["data_server"].items():
        for ii in range(len(bc)):
            if server in bc[ii]:
                return bc[ii][server], i
            else:
                return None


# print(nama_server("v2ay2.udpgw.com"))
# %%
# untuk generate dari database


def generate(jenis, mode, tipe):
    db = []
    with open("log.json") as json_files:
        data = json.load(json_files)
        akun_parsing = data["akun_parsing"]
        data_bug = data["data_bug"]
        data_bug_set = set(data_bug)
        if jenis == "vmess":
            read_db = akun_parsing["vmess"]
            for i in range(len(read_db)):
                cm = read_db[i]
                dt = {}
                search = [cm['add'], cm['sni'], cm['ps'], cm['host']]
                for item in search:
                    if "." in item and item not in data_bug_set:
                        try:
                            dd = nama_server(item)[0]
                            db_server = item
                        except TypeError:
                            db_server = f"{item}"
                            dd = db_server+"-"+generate_random_string(6)
                if mode == "gamemax":
                    bug = "cf-vod.nimo.tv"
                    if tipe == "lama":
                        dt['name'] = f"{dd}-gm"
                        dt['server'] = bug
                        dt['port'] = 8080
                        dt['type'] = 'vmess'
                        dt['uuid'] = cm['id']
                        dt['alterId'] = 0
                        dt['cipher'] = 'auto'
                        dt['tls'] = 'false'
                        dt['skip-cert-verify'] = 'true'
                        cm['sni'] = db_server
                        dt['servername'] = cm['sni']
                        if cm['net'] == "grpc":
                        	dt['network'] = 'grpc'
                        	dt['grpc-opts'] = {'grpc-service-name': cm['path']}
                        	dt['port'] = 443
                        	dt['tls'] = 'true'
                        if cm['net'] == "ws":
                            dt['network'] = 'ws'
                            cm["host"] = db_server
                            dt['ws-opts'] = {'path': cm['path'],
                                         'headers': {'Host': db_server}}
                        dt['udp'] = 'true'
                    if tipe == "baru":
                        dt['name'] = f"{dd}-gmb"
                        dt['server'] = bug
                        dt['port'] = 443
                        dt['type'] = 'vmess'
                        dt['uuid'] = cm['id']
                        dt['alterId'] = 0
                        dt['cipher'] = 'auto'
                        dt['tls'] = 'true'
                        dt['skip-cert-verify'] = 'true'
                        dt['servername'] = bug
                        dt['network'] = 'ws'
                        cm["host"] = db_server
                        dt['ws-opts'] = {'path': f'GET-:wss://{bug}/fastssh/',
                                         'headers': {'Host': cm['host']}}
                        dt['udp'] = 'true'
                if mode == "opok":
                    bug = "corona.jakarta.go.id"
                    if tipe == "lama":
                        dt['name'] = f"{dd}-op"
                        dt['server'] = bug
                        dt['port'] = 443
                        dt['type'] = 'vmess'
                        dt['uuid'] = cm['id']
                        dt['alterId'] = 0
                        dt['cipher'] = 'auto'
                        dt['tls'] = 'true'
                        dt['skip-cert-verify'] = 'true'
                        cm['sni'] = bug
                        dt['servername'] = cm['sni']
                        dt['network'] = 'ws'
                        if cm["host"] in data_bug:
                            cm["host"] = db_server
                        dt['ws-opts'] = {'path': f"wss://{bug}{cm['path']}",
                                         'headers': {'Host': cm['host']}}
                        dt['udp'] = 'true'
                    if tipe == "baru":
                        dt['name'] = f"{dd}-opb"
                        dt['server'] = bug
                        dt['port'] = 443
                        dt['type'] = 'vmess'
                        dt['uuid'] = cm['id']
                        dt['alterId'] = 0
                        dt['cipher'] = 'auto'
                        dt['tls'] = 'true'
                        dt['skip-cert-verify'] = 'true'
                        dt['servername'] = bug
                        dt['network'] = 'ws'
                        cm["host"] = db_server
                        dt['ws-opts'] = {'path': f'GET-:wss://{bug}/fastssh/',
                                         'headers': {'Host': cm['host']}}
                        dt['udp'] = 'true'
                    if tipe == "worry":
                        dt['name'] = f"{dd}-opw"
                        dt['server'] = db_server
                        dt['port'] = 80
                        dt['type'] = 'vmess'
                        dt['uuid'] = cm['id']
                        dt['alterId'] = 0
                        dt['cipher'] = 'auto'
                        dt['tls'] = 'false'
                        dt['skip-cert-verify'] = 'false'
                        dt['servername'] = "tsel.me"
                        dt['network'] = 'ws'
                        if cm["host"] in data_bug:
                            cm["host"] = data_bug
                        dt['ws-opts'] = {'path': "/worryfree",
                                         'headers': {'Host': "tsel.me"}}
                        dt['udp'] = 'true'
                db.append(dt)
        if jenis == "trojan":
            read_db = akun_parsing["trojan"]
            for i in range(len(read_db)):
                cm = read_db[i]
                dt = {}
                search = [cm['server'], cm['sni'], cm['host']]
                for item in search:
                    if "." in item and item not in data_bug_set:
                        try:
                            dd = nama_server(item)[0]
                            db_server = item
                        except TypeError:
                            db_server = f"{item}"
                            dd = db_server+"-"+generate_random_string(6)
                if mode == "gamemax":
                    bug = "cf-vod.nimo.tv"
                    if tipe == "lama":
                        dt['name'] = f"{dd}-gm"
                        dt['server'] = bug
                        dt['port'] = 443
                        dt['type'] = 'trojan'
                        dt['password'] = cm['password']
                        dt['tls'] = 'true'
                        dt['skip-cert-verify'] = 'true'
                        dt['sni'] = db_server
                        if cm['type'] == "grpc":
                            dt['network'] = 'grpc'
                            dt['grpc-opts'] = {'grpc-service-name': cm['grpc-service-name']}
                        if cm['type'] == "ws":
                            dt['network'] = 'ws'
                            dt['ws-opts'] = {'path': cm['path'],
                                         'headers': {'Host': cm['host']}}
                        dt['udp'] = 'true'
                if mode == "opok":
                    bug = "corona.jakarta.go.id"
                    if tipe == "lama":
                        dt['name'] = f"{dd}-op"
                        dt['server'] = bug
                        dt['port'] = 443
                        dt['type'] = cm['type']
                        dt['password'] = cm['password']
                        dt['tls'] = 'true'
                        dt['skip-cert-verify'] = 'true'
                        dt['sni'] = cm['host']
                        dt['network'] = 'ws'
                        dt['ws-opts'] = {'path': cm['path'],
                                         'headers': {'Host': cm['host']}}
                        dt['udp'] = 'true'
                db.append(dt)
        if jenis == "ss":
            read_db = akun_parsing["ss"]
            for i in range(len(read_db)):
                cm = read_db[i]
                dt = {}
                search = [cm['server'], cm['host']]
                for item in search:
                    if "." in item and item not in data_bug_set:
                        try:
                            dd = nama_server(item)[0]
                            db_server = item
                        except TypeError:
                            db_server = f"{item}"
                            dd = db_server+"-"+generate_random_string(6)
                if mode == "gamemax":
                    bug = "cf-vod.nimo.tv"
                    if tipe == "lama":
                        dt['name'] = f"{dd}-gm"
                        dt['server'] = bug
                        dt['port'] = 80
                        dt['type'] = 'ss'
                        dt['cipher'] = cm['cipher']
                        dt['password'] = f"'{cm['password']}'"
                        dt['udp-over-tcp'] = 'true'
                        dt['plugin'] = 'v2ray-plugin'
                        dt['plugin-opts'] = {'mode': 'websocket', 'host': cm['server'],
                                             'path': cm['path'], 'tls': 'false', 'skip-cert-verify': 'true', 'mux': 'true'}
                if mode == "opok":
                    bug = "corona.jakarta.go.id"
                    if tipe == "lama":
                        dt['name'] = f"{dd}-op"
                        dt['server'] = bug
                        dt['port'] = 443
                        dt['type'] = 'ss'
                        dt['cipher'] = cm['cipher']
                        dt['password'] = f"'{cm['password']}'"
                        dt['udp-over-tcp'] = 'true'
                        dt['plugin'] = 'v2ray-plugin'
                        dt['plugin-opts'] = {
                            'mode': 'websocket',
                            'host': cm['server'],
                            'path': f"wss://{bug}{cm['path']}",
                            'tls': 'true',
                            'skip-cert-verify': 'true',
                            'mux': 'true',
                            'sni': bug
                        }
                db.append(dt)
    return db

# %%
# read_generate = generate("vmess", "gamemax", "lama")
# write_config untuk menulis config.yaml yang sudah di generate


def write_config(read_generate):
    with open('config.yaml', 'w') as yaml_file:
        yaml.dump([{"proxies": read_generate}],
                  yaml_file, sort_keys=False)
    with open('config.yaml', 'r') as yaml_file2:
        update = yaml_file2.read().replace(
            "'true'", "true").replace("- proxies:", "proxies:").replace("'false'", "false")
        with open('config.yaml', 'w') as yaml_file3:
            yaml_file3.write(update)

# result untuk menampilkan hasil akhir dari config.yaml


def result():
    with open('config.yaml', 'r') as yaml_file:
        cetak = yaml_file.read()
        print(cetak)
        return cetak
# write_config(read_generate)
