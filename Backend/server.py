from flask import Flask, request, jsonify
from NN_classifier import predict_malicious

app = Flask(__name__)

# Маршрут для принятия URL и возврата оценки вредоносности
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data['url']
    f = open('text.txt', 'w')
    f.write(url + '\n')
    f.close()
    result = predict_malicious(url)  # Вызов функции для оценки вредоносности
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(port=5000)