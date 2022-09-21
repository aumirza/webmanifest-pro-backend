from io import BytesIO
from flask import Flask, jsonify, request, send_file
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin

from bot import getTelegramFile, sendDocument, sendMessage
from utils.image_generator import generate_images_zip
from utils import allowed_file


load_dotenv()
app = Flask(__name__)
cors = CORS(app)
# resources={r"/api/*": {"origins": "*"}}


@app.route('/bot/post/', methods=['POST'])
async def webhookMessageHandler():
    data = request.get_json()

    if not 'message' in data:
        return jsonify({'status': 'ok - no message'})

    message = data['message']

    chat_id = message['chat']['id']

    if 'text' in message:
        text = message['text']

        if text == '/start':
            return jsonify({
                'method': 'sendMessage',
                'chat_id': chat_id,
                'text': 'Hi there! Send me a picture and \nI will generate different size images for webApp.'
            })

        else:
            return jsonify({
                'method': 'sendMessage',
                'chat_id': chat_id,
                'text': 'I am not your assistant.'
            })

    elif set(['photo', 'sticker']).issubset(message.keys()):

        sendMessage(chat_id, 'Generating images...')

        if 'photo' in message:
            photo = message['photo']
            file_id = photo[-1]['file_id']
        elif 'sticker' in message:
            sticker = message['sticker']
            file_id = sticker['file_id']
        else:
            return jsonify({'status': 'ok - no photo or sticker'})

        image = getTelegramFile(file_id)

        print('Generating images...')
        zip_path = await generate_images_zip(image)
        print('returning zip file')
        sendDocument(chat_id, zip_path)

        return jsonify({'status': 'ok'})

    return jsonify({
        'method': 'sendMessage',
        'chat_id': chat_id,
        'text': 'This too hot to handle.'
    })


@app.route('/api/upload', methods=['POST', 'OPTIONS'])
async def main():

    image = request.files.get('image')

    if image and allowed_file(image.filename):
        image = BytesIO(image.stream.read())
        zip_path = await generate_images_zip(image)
        return send_file(zip_path, download_name='images.zip', as_attachment=True)

    return jsonify({'message': 'No images given'}), 404


if __name__ == '__main__':
    app.run(debug=True)
