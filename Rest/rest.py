#!flask/bin/python
import six
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth

app=Flask(__name__, static_url_path="")
auth=HTTPBasicAuth()



#atencao:
#elephant=elefante
#mouse=rato
#turtle=tartaruga
#dragonfly=libelula
#xita=guepardo
#conch=caramujo

#lista simulando fluxos para testes
pkts = [
        {'id': 1, 'protocolo': "http", 'duracao':"turtle", 'tamanho': "elephant", 'taxa': "conch"},
        {'id': 2, 'protocolo': "ssh", 'duracao': "dragonfly", 'tamanho': "mouse", 'taxa': "xita"},
        {'id': 3, 'protocolo': "dhcp", 'duracao': "turtle", 'tamanho': "elephant", 'taxa': "conch"},
        {'id': 4, 'protocolo': "torrent", 'duracao': "dragonfly", 'tamanho': "mouse", 'taxa': "xita"},
        {'id': 5, 'protocolo': "ssdp", 'duracao': "turtle", 'tamanho': "elephant", 'taxa': "conch"},
        {'id': 6, 'protocolo': "ssh", 'duracao': "dragonfly", 'tamanho': "mouse", 'taxa': "xita"},
        {'id': 7, 'protocolo': "ssl", 'duracao': "turtle", 'tamanho': "elephant", 'taxa': "conch"},
        {'id': 8, 'protocolo': "dhcp", 'duracao': "dragonfly", 'tamanho': "mouse", 'taxa': "xita"},
        {'id': 9, 'protocolo': "ssdp", 'duracao': "turtle", 'tamanho': "elephant", 'taxa': "conch"},
        {'id': 10, 'protocolo': "dhcp", 'duracao': "dragonfly", 'tamanho': "mouse", 'taxa': "xita"},
        {'id': 11, 'protocolo': "http", 'duracao': "dragonfly", 'tamanho': "mouse", 'taxa': "conch"},
        ]


#autenticacao no rest
@auth.get_password
def get_password(username):
    if username=='admin':
        return 'clarissa'
    return None





@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)




@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)





@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



#retorna a porcentagem de tartarugas e libélulas e elefantes de um [protocolo]
@app.route('/rest/api/<string:protocolo>/duracao', methods=['GET'])
@auth.login_required
def get_duracao(protocolo):
    count_turtle=0
    count_dragonfly=0
    duracaoPkts=[pkt for pkt in pkts if pkt['protocolo'] == protocolo]
    if len(duracaoPkts)==0:
        abort(404)
    for pkt in duracaoPkts:
        if pkt['duracao']=='turtle':
            count_turtle+=1
        if pkt['duracao']== 'dragonfly':
            count_dragonfly += 1
    return jsonify({'%s por duracao' % protocolo.upper():
        [{'Quantidade Tartarugas':count_turtle}, {'Quantidade Libelulas':count_dragonfly},
        {'Pocentagem Tartarugas':float(100*count_turtle/(count_turtle+count_dragonfly))},
        {'Pocentagem Libelulas':float(100*count_dragonfly/(count_turtle+count_dragonfly))}]})






#retorna a porcentagem de ratos e elefantes de um [protocolo]
@app.route('/rest/api/<string:protocolo>/tamanho', methods=['GET'])
@auth.login_required
def get_tamanho(protocolo):
    count_elephant=0
    count_mouse=0
    tamanhoPkts=[pkt for pkt in pkts if pkt['protocolo'] == protocolo]
    if len(tamanhoPkts) == 0:
        abort(404)
    for pkt in tamanhoPkts:
        if pkt['tamanho']== 'elephant':
            count_elephant += 1
        if pkt['tamanho']== 'mouse':
            count_mouse += 1
    return jsonify({'%s por tamanho' % protocolo.upper():
        [{'Quantidade Elefantes':count_elephant}, {'Quantidade Ratos':count_mouse},
        {'Pocentagem Elefantes':float(100*count_elephant/(count_elephant+count_mouse))},
        {'Pocentagem Ratos':float(100*count_mouse/(count_elephant+count_mouse))}]})







#retorna a porcentagem de guepardos e caramujos de um [protocolo]
@app.route('/rest/api/<string:protocolo>/taxa', methods=['GET'])
@auth.login_required
def get_taxa(protocolo):
    count_xita=0
    count_conch=0
    taxaPkts=[pkt for pkt in pkts if pkt['protocolo'] == protocolo]
    if len(taxaPkts) == 0:
        abort(404)
    for pkt in taxaPkts:
        if pkt['taxa']== 'xita':
            count_xita += 1
        if pkt['taxa']== 'conch':
            count_conch += 1
    return jsonify({'%s por taxa' % protocolo.upper():
        [{'Quantidade Guepardos':count_xita}, {'Quantidade Caramujos':count_conch},
        {'Pocentagem Guepardos':float(100*count_xita/(count_xita+count_conch))},
        {'Pocentagem Caramujos':float(100*count_conch/(count_xita+count_conch))}]})





#retorna a porcentagem dos protocolos que são [animal]
@app.route('/rest/api/<string:animal>', methods=['GET'])
@auth.login_required
def get_animal(animal):
    count_torrent = 0
    count_dhcp = 0
    count_http = 0
    count_ssdp = 0
    count_ssh = 0
    count_ssl = 0
    pkts_animal = [pkt for pkt in pkts if pkt['tamanho'] == animal or pkt['duracao'] == animal or pkt['taxa'] == animal]
    if len(pkts_animal) == 0:
        abort(404)
    for pkt in pkts_animal:
        if pkt['protocolo']=='torrent':
            count_torrent += 1
        if pkt['protocolo']=='dhcp':
            count_dhcp += 1
        if pkt['protocolo']=='http':
            count_http += 1
        if pkt['protocolo']=='ssdp':
            count_ssdp += 1
        if pkt['protocolo']=='ssh':
            count_ssh += 1
        if pkt['protocolo']=='ssl':
            count_ssl += 1
    return jsonify({'%s por protocolo' % animal.upper():
            [
                {'Quantidade torrent':count_torrent}, {'Quantidade dhcp':count_dhcp},
                {'Quantidade http':count_http}, {'Quantidade ssdp':count_ssdp}, {'Quantidade ssh':count_ssh}, {'Quantidaded ssl':count_ssl},
                {'Pocentagem torrent':float(100*count_torrent/(count_torrent+count_dhcp+count_http+count_ssdp+count_ssh+count_ssl))},
                {'Pocentagem dhcp':float(100*count_dhcp/(count_torrent+count_dhcp+count_http+count_ssdp+count_ssh+count_ssl))},
                {'Pocentagem http':float(100*count_http/(count_torrent+count_dhcp+count_http+count_ssdp+count_ssh+count_ssl))},
                {'Pocentagem ssdp':float(100*count_ssdp/(count_torrent+count_dhcp+count_http+count_ssdp+count_ssh+count_ssl))},
                {'Pocentagem ssh':float(100*count_ssh/(count_torrent+count_dhcp+count_http+count_ssdp+count_ssh+count_ssl))},
                {'Pocentagem ssl':float(100*count_ssl/(count_torrent+count_dhcp+count_http+count_ssdp+count_ssh+count_ssl))}
            ]
        })






def make_public_pkt(pkt):
    new_pkt = {}
    for field in pkt:
        if field == 'id':
            new_pkt['uri'] = url_for('get_pkt', pkt_id=pkt['id'],
                                      _external=True)
        else:
            new_pkt[field] = pkt[field]
    return new_pkt


#inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)
