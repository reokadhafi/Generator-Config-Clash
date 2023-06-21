import webbrowser as wb
from clash1 import write_database, add_akun, clear_akun, generate, write_config, result
from flask import Flask, render_template, request

url = "http://127.0.0.1:5000"


def runbrowser(urls):
    wb.open(urls)


application = Flask(__name__)

# Function baru di bawah ini


@application.route('/', methods=['GET', 'POST'])
def index():
    dbakun = "None"
    mode = ""
    if request.method == 'POST':
        if request.form.get('save') == 'Save':
            akunn = request.form['akun']
            file_db = open(('db_save.txt'), "a+")
            file_db.write(f"{akunn}\n")
            file_db.close()
            write_database(add_akun(akunn))
        elif request.form.get('clear') == 'Clear Data':
            file_db = open(('db_save.txt'), "w")
            file_db.write("")
            file_db.close()
            write_database(clear_akun("vmess"))
            write_database(clear_akun("trojan"))
            write_database(clear_akun("ss"))
        elif request.form.get('generate') == 'Generate':
            # dbakun = write_config(generate(request.form["modemode"].split(",")[
            #     0], request.form["modemode"].split(",")[1], request.form["modemode"].split(",")[2]))
            write_config(generate(request.form["modemode"].split(",")[
                0], request.form["modemode"].split(",")[1], request.form["modemode"].split(",")[2]))
            dbakun = result()
            mode = request.form["modemode"].split(",")
        # return render_template('index.html', akunn=akunn, dbakun=dbakun)
    return render_template('index.html', dbakun=dbakun, mode=mode)


runbrowser(url)
if __name__ == '__main__':
    application.run(debug=True)
