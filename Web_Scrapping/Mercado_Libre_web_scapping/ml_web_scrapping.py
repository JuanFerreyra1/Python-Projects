import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os 






def read_variables():
    path = ''
    if os.path.exists(path):
        with open(path, 'r') as archivo:
            valor = archivo.read().strip()
    else:
        valor = str()
    return valor,path


def get_access_token(variable,path):
    url = 'https://api.mercadolibre.com/oauth/token'
    data = {
        'refresh_token':f'{variable}',
        'grant_type':'refresh_token',
        'client_id':'',
        'client_secret':''}
    token_and_refresh_token = requests.post(url, data=data)
    token_and_refresh_token = json.loads(token_and_refresh_token.text)
    with open(path, 'w') as archivo:
        archivo.write(token_and_refresh_token["refresh_token"])
    
    return token_and_refresh_token["access_token"]


def search_product(token,string_to_query):
    url =  f'https://api.mercadolibre.com/sites/MLA/search?category=1744&q={string_to_query}&since=today'
    headers = {
        'Authorization':f'Bearer {token}'
    }
    search_result = requests.get(url, headers=headers)
    search_output = json.loads(search_result.text)
    output =  []
    c = 0
    for x in search_output.get('results'):
        c+=1
        title = 'Post Nº'+str(c)
        item_dict = {}
        item_sub_dict = {}
        item_sub_dict['link'] = x.get('permalink')
        price = x.get('price')
        if len(str(price)) > 5:
            item_sub_dict['precio'] = '$' + str(price)
        else:
            item_sub_dict['precio'] = str(price) + ' usd'
        item_dict[title] = item_sub_dict
        kilometers = next((item['value_name'] for item in x.get('attributes', []) if item.get('id') == 'KILOMETERS'),None)
        item_sub_dict['kilometros'] = kilometers
        year = next((item['value_name'] for item in x.get('attributes', []) if item.get('id') == 'VEHICLE_YEAR'),None)
        item_sub_dict['año'] = year
        output.append(item_dict)

    output = json.dumps(output, indent=2, ensure_ascii=False)

    return output


def send_email(result):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = ''  
    smtp_password = ''

    # Configuración del correo
    sender_email = ''
    receiver_email = ['']
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    subject = f'GOL TREND PUBLICADOS HOY - {today}'
    
    # Crear el cuerpo del correo
    body = f'Hoy se publicaron los siguientes gol trend: \n{result}'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Conectar al servidor SMTP y enviar el correo
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())





if __name__ == "__main__":
    variable, path = read_variables()
    token = get_access_token(variable,path)
    result = search_product(token,'goltrend')
    send_email(result)