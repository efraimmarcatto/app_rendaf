from app import app
from datetime import datetime
from flask import request, jsonify
from app.models.transactions import Transactions

@app.route('/')
def index():
    return '''<h1>API de Teste em Python usando Flask e Flask-MongoEngine</h1>
    <h1>Rotas</h1>
<hr />
<table border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<th style="width: 95px;">Endpoint</th>
<th style="width: 76px;">Method</th>
<th style="width: 131px;">Regra</th>
</tr>
<tr>
<td style="width: 95px;">&nbsp;search</td>
<td style="width: 76px;">&nbsp;POST</td>
<td style="width: 131px;">&nbsp;/search</td>
</tr>
<tr>
<td style="width: 95px;">&nbsp;show</td>
<td style="width: 76px;">&nbsp;GET</td>
<td style="width: 131px;">&nbsp;/show/&lt;id&gt;</td>
</tr>
<tr>
<td style="width: 95px;">&nbsp;store</td>
<td style="width: 76px;">&nbsp;POST</td>
<td style="width: 131px;">&nbsp;/store</td>
</tr>
<tr>
<td style="width: 95px;">&nbsp;update</td>
<td style="width: 76px;">&nbsp;PUT</td>
<td style="width: 131px;">&nbsp;/update/&lt;id&gt;</td>
</tr>
<tr>
<td style="width: 95px;">&nbsp;delete</td>
<td style="width: 76px;">&nbsp;DELETE</td>
<td style="width: 131px;">
<p>&nbsp;/delete/&lt;id&gt;</p>
</td>
</tr>
</tbody>
</table>
<h1>Uso</h1>
<hr />
<h2>/search</h2>
<p>Pode receber um JSON contendo value e date.</p>
<p>Exemplo:</p>
<p style="padding-left: 30px;">{</p>
<p style="padding-left: 60px;">"date" : "2019-09-02 00:11:50",</p>
<p style="padding-left: 60px;">"value" : 200</p>
<p style="padding-left: 30px;">}</p>
<p>Se n&atilde;o for enviado nenhum parametro, &eacute; retornado todas as transa&ccedil;&otilde;es cadastradas.</p>
<p>Se for enviado uma data e um valor s&atilde;o exibidos todas as transa&ccedil;&otilde;es ap&oacute;s a data e com o valor minimo estipulado.</p>
<h2>/show/id</h2>
<p>&nbsp;Mostra o registro correspondente ao id informado na URL, sendo a id um ObjectId.</p>
<p>&nbsp;</p>
<h2>/store</h2>
<p>Recebe um JSON, obrigatoriamente, contendo sourceAccount, destinationAccount e value.</p>
<p>Exemplo:</p>
<p style="padding-left: 30px;">{</p>
<p style="padding-left: 60px;">"destinationAccount" : "123456",</p>
<p style="padding-left: 60px;">"sourceAccount" : "654321",</p>
<p style="padding-left: 60px;">"value" : 12000</p>
<p style="padding-left: 30px;">}</p>
<h2>/update/id</h2>
<p>Pode receber um JSON contendo sourceAccount, destinationAccount e value. As chaves informadas ser&atilde;o atualizadas do registro correspondente ao id informado na URL, sendo a id um ObjectId.</p>
<p>Exemplo:</p>
<p style="padding-left: 30px;">{</p>
<p style="padding-left: 60px;">"destinationAccount" : "123456",</p>
<p style="padding-left: 60px;">"sourceAccount" : "654321",</p>
<p style="padding-left: 60px;">"value" : 12000</p>
<p style="padding-left: 30px;">}</p>
<h2>/delete/id</h2>
<p>Remove o registro do banco de dados correspondente ao id informado na URL, sendo a id um ObjectId.</p>
<p>&nbsp;</p>'''

@app.route('/search', methods=['POST'])
def search():
    
    if request.json== None:
        transactions = Transactions.objects()
       
    else:
        data = request.get_json()
        transactions = Transactions.objects(value__gte=data['value'], createdDate__gte=data['date'])
        
    return jsonify(transactions)
    


@app.route('/show/<id>')
def show(id):
    transaction = Transactions.objects(id=id)
    return jsonify(transaction)

@app.route('/store', methods=['POST'])
def store():
    
        data = request.get_json()
        if 'sourceAccount' in data and 'destinationAccount' in data and 'value' in data:
            try:
                transaction = Transactions(
                    sourceAccount = data['sourceAccount'],
                    destinationAccount=data['destinationAccount'],
                    value=data['value']
                    ).save()
                return jsonify({'message':'Transaction added.'}), 201
            except:
                return jsonify({'error':'Problem to add transaction.'}), 500
        else:
            return jsonify({'error':'Missing parameters'}), 500




@app.route('/update/<id>', methods=['PUT'] )
def update(id):
    transaction = Transactions.objects(id=id)
    
    if transaction:
        data = request.get_json()
        if 'value' in data:
            transaction.update(value=data['value'])

        if 'sourceAccount' in data:
            transaction.update(sourceAccount=data['sourceAccount'])
        
        if 'destinationAccount' in data:
            transaction.update(destinationAccount = data['destinationAccount'])


        return jsonify(transaction)

    else:
        return jsonify({'message':'Transaction not Found'}), 404
        

@app.route('/delete/<id>', methods=['DELETE'] )
def delete(id):
    transaction = Transactions.objects(id=id)
    if transaction:
        transaction.delete()
        return jsonify({'message':'Transaction removed'})
    else:
        return jsonify({'error':'Transaction not Found'})
