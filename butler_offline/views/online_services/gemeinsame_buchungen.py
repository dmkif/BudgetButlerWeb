from butler_offline.viewcore import requester
import json


def get_gemeinsame_buchungen(serverurl, email, password):
    jsondata = requester.instance().post(serverurl + '/gemeinsamebuchung.php',
                                         data={'email': email, 'password': password})
    return json.loads(jsondata)


def upload_gemeinsame_buchungen(serverurl, data, auth_container):
    jsondata = requester.instance().put(serverurl + '/gemeinsamebuchung.php', data, auth_container.cookies())
    return json.loads(jsondata)['result'] == 'OK'
