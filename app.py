from flask import Flask, render_template,request,redirect, jsonify
from pagamento import gerarpagamento
from dotenv import load_dotenv
import os
import mercadopago
import sqlite3


load_dotenv()
sdkk = os.getenv("SDK2")
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pagamento',methods=['POST'])
def pagamentos():
    valor = request.form.get('valor')
    titulo = request.form.get('titulo')
    id = request.form.get('id')
    return render_template('ogin.html',valor=valor,titulo=titulo, id=id)

@app.route('/pagar',methods=['POST'])
def pagar():
    nome=request.form.get('nome')
    numero=request.form.get('numero')
    valor = request.form.get('valor')
    titulo = request.form.get('titulo')
    id = request.form.get('id')
    #print(nome,numero,valor,titulo)
    valor=float(valor)
    #print(type(valor))
    link = gerarpagamento(nome,numero,valor,titulo,id)
    return redirect(link)

@app.route('/compra_certa')
def compra_certa():
    return render_template('acerto.html')

@app.route('/compra_errada')
def compra_errada():
    return render_template('erro.html')

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()  # Recebe os dados enviados pelo MercadoPago
    print(f"PAGAMENTO CHEGOU \n{data}")
    if not data:
        return jsonify({"error": "Nenhum JSON recebido"}), 400

    payment_id = data.get("data", {}).get("id")
    if not payment_id:
        return jsonify({"error": "ID do pagamento não encontrado"}), 400

    # Consulta os detalhes do pagamento
    sdk = mercadopago.SDK(sdkk)
    payment_info = sdk.payment().get(payment_id)
    status_pagamento = payment_info["response"].get("status")
    if "response" not in payment_info:
        return jsonify({"error": "Erro ao consultar pagamento"}), 500
    
    external_reference = payment_info["response"].get("external_reference")
    status_pagamento = payment_info["response"].get("status")

    print(external_reference)
    print(status_pagamento)

    """conn = sqlite3.connect("pagamentoss")
    cur = conn.cursor()"""
    #cur.execute("SELECT * FROM pagamentosbarbearia WHERE txid = ?", (external_reference,))
    #j = cur.fetchone()
    #print(j)
    if status_pagamento == "approved":
        return redirect("http://127.0.0.1:5000/compra_certa")
        """cur.execute("UPDATE pagamentosbarbearia SET status=? WHERE txid=?", (status_pagamento, external_reference))
        conn.commit()
        conn.close()"""
        print("STATUS ATUALIZADO APROVADO")
    """elif status_pagamento == "rejected":
        cur.execute("DELETE FROM pagamentosbarbearia WHERE txid=?", (external_reference,))
        conn.commit()
        conn.close()
        print("REJEITADO EXCLUINDO DO BANCO")"""
    
    """if j and j[1] == "pendente":
        cur.execute("UPDATE pagamentosbarbearia SET status = ? WHERE txid = ?", ("PAGO", external_reference))
        conn.commit()
        print("ATT COM SUCESSO")

        return render_template("cok.html")"""
    
    return jsonify({"message": "Webhook processado com sucesso"}), 200  # Retorna sucesso
