import mercadopago
from datetime import datetime, timedelta
import uuid
from dotenv import load_dotenv
import os

load_dotenv()
sdkk = os.getenv("SDK2")
email = "USERTESTEEMAIL222222.COM"
def gerarpagamento(nome,numero,valor,titulo,id):
    #valor = 1.0
    id = int(id)
    if id == 1:
        valor = 75
        titulo = "Plano Mensal Corte"
    elif id == 2:
        valor = 130
        titulo = "Plano Mensal Corte é Barba"
    else:
        valor = 10000
        titulo = "ESPERTINHO VC"
    external_reference = str(uuid.uuid4())
    tt = "plano mensal cabelo"

    #sdk = mercadopago.SDK("TEST-7006907603533943-021514-d78959114578f0e324a55082a506b45f-210051360")#CLODOALDO
    #sdk = mercadopago.SDK("TEST-8397555859715214-022022-44cea229d8798f47f1c7c38bfa5968a1-441212954")#credencias testeSEBASTIAN
    sdk = mercadopago.SDK(sdkk)
    payment_data = {
        "items": [
            {"id": "1", "title": titulo, "quantity": 1, "currency_id": "BRL", "unit_price": valor},
        ],

        "payer": {  # Adicionando nome e telefone do comprador
        "name": nome,  # Substitua pelo nome do comprador
        "phone": {
            "area_code": "81",  # Substitua pelo código de área
            "number": numero  # Substitua pelo número de telefone
            }
        },
        "back_urls": {
            "success": "https://e2b1-160-20-194-29.ngrok-free.app/compra_certa",
            "failure": "https://e2b1-160-20-194-29.ngrok-free.app/compra_errada",
            "pending": "https://e2b1-160-20-194-29.ngrok-free.app/compra_errada",
        },
        "auto_return": "all",
        "external_reference": external_reference,  # Substitua pelo valor adequado
        "notification_url": "https://e2b1-160-20-194-29.ngrok-free.app/webhook",

        # Definir métodos de pagamento
        "payment_methods": {
            "excluded_payment_types": [
                {"id": "ticket"},  # Exclui pagamento por boleto
                {"id": "debit_card"}  # Exclui cartões de débito
            ],
            # Caso queira configurar parcelas ou outros parâmetros específicos de cartão de crédito ou PIX
        }
    }
    result = sdk.preference().create(payment_data)
    payment = result["response"]
    linkpagar = payment["init_point"]
    payment_id = payment.get("external_reference")
    payment_payer = payment.get("payer")
    print(payment_id)
    print(payment_payer)
    data_compra = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #cur.execute("INSERT INTO pagamentosbarbearia (txid, status, email, data_compra, plano) VALUES(?,?,?,?,?)", (external_reference, "pendente", email, data_compra,tt))
    return linkpagar
