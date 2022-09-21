from io import BytesIO
import requests
from config import DOMAIN, TOKEN

telegramUrl = "https://api.telegram.org/bot" + TOKEN
fileUrl = "https://api.telegram.org/file/bot" + TOKEN + "/"
webAppUrl = DOMAIN+"bot/post/"


def setWebhook():
    url = telegramUrl + "/setWebhook?url=" + webAppUrl
    response = requests.get(url)
    print(response.json())


def sendMessage(chat_id, text):
    url = telegramUrl + "/sendMessage?chat_id=" + \
        str(chat_id) + "&text=" + text
    response = requests.get(url)


def getTelegramFilepath(file_id):
    url = telegramUrl + "/getFile?file_id=" + file_id
    response = requests.get(url)
    return fileUrl + response.json()['result']['file_path']


def getTelegramFile(file_id):
    response = requests.get(getTelegramFilepath(file_id))
    return BytesIO(response.content)


def sendDocument(chat_id, document):
    url = telegramUrl + "/sendDocument?chat_id=" + str(chat_id)
    files = {'document': open(document, 'rb')}
    response = requests.post(url, files=files)


if __name__ == '__main__':
    setWebhook()
