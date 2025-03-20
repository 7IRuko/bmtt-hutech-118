from flask import Flask, request, jsonify
from cipher.ecc import ECCCipher  # Thêm vào đầu file

app = Flask(__name__)

# ECC CIPHER ALGORITHM
ecc_cipher = ECCCipher()

@app.route('/api/ecc/generate_keys', methods=['GET'])
def generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign_message():
    data = request.json
    message = data['message']
    
    private_key, _ = ecc_cipher.load_keys()
    signature = ecc_cipher.sign(message, private_key)
    signature_hex = signature.hex()
    
    return jsonify({'signature': signature_hex})

@app.route('/api/ecc/verify', methods=['POST'])
def ecc_verify_signature():
    data = request.json
    message = data['message']
    signature_hex = data['signature']
    
    _, public_key = ecc_cipher.load_keys()
    signature = bytes.fromhex(signature_hex)
    
    is_verified = ecc_cipher.verify(message, signature)
    
    return jsonify({'is_verified': is_verified})

# Main function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
