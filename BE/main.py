from quart import Quart, request, jsonify
from quart_cors import cors
from middleware.custom_error import CustomError
from middleware.custom_response import CustomResponse
import algorithm.rctm_Elgamal as RCTM
import algorithm.rk4_elgamal_real as RK4
import algorithm.nist_test as NIST
import asyncio
import time

HOST='localhost'
PORT=4000

public_key, private_key = RCTM.elgamal_key_generation()
model, seed = RK4.generate_model()

app = Quart(__name__)

app = cors(app, allow_origin="*")

@app.route('/', methods=['GET'])
def home():
    return 'healthcheck: healthy💫'

@app.route('/rctm', methods=['POST'])
async def doRCTM():
    try:
        req = await request.get_json()

        if req['message'] is None or req['message'] == "":
            raise CustomError(400, 'message required')
        
        global private_key
        global public_key

        int_message = RCTM.string_to_integer(str(req['message']))
        
        enc_start_time = time.time()
        encrypt_result, bitstream = RCTM.elgamal_encrypt(int_message, public_key)
        enc_duration = time.time() - enc_start_time

        test_result = NIST.do_nist_test_and_return(bitstream)

        dec_start_time = time.time()
        decrypt_result = RCTM.elgamal_decrypt(encrypt_result, private_key, public_key)
        dec_duration = time.time() - dec_start_time

        str_message = RCTM.integer_to_string(int(decrypt_result))

        result = {
            "original": str(req['message']),
            "encryption": encrypt_result,
            "decryption": str_message,
            "enc_duration": f"{enc_duration:.16f}",
            "dec_duration": f"{dec_duration:.16f}",
            "nist_test_result": test_result
        }

        response = CustomResponse(200, 'RCTM successfully analyzed', result)
        return jsonify(response.JSON()), response.code
    except Exception as err:
        print(err)
        return jsonify(err.JSON()), err.code

@app.route('/rk4', methods=['POST'])
async def doRK4():
    try:
        req = await request.get_json()

        if req['message'] is None or req['message'] == "":
            raise CustomError(400, 'message required')
        
        global private_key
        global public_key
        global model
        global seed

        int_message = RK4.string_to_integer(str(req['message']))

        enc_start_time = time.time()
        encrypt_result, bitstream = RK4.elgamal_encrypt(int_message, public_key, model, seed)
        enc_duration = time.time() - enc_start_time

        test_result = NIST.do_nist_test_and_return(bitstream)

        dec_start_time = time.time()
        decrypt_result = RK4.elgamal_decrypt(encrypt_result, private_key, public_key)
        dec_duration = time.time() - dec_start_time

        str_message = RK4.integer_to_string(int(decrypt_result))
        
        result = {
            "original": str(req['message']),
            "encryption": encrypt_result,
            "decryption": str_message,
            "enc_duration": f"{enc_duration:.16f}",
            "dec_duration": f"{dec_duration:.16f}",
            "nist_test_result": test_result
        }

        response = CustomResponse(200, 'RK4 successfully analyzed', result)
        return jsonify(response.JSON()), response.code
    except Exception as err:
        print(err)
        return jsonify(err.JSON()), err.code

if __name__ == '__main__':
    asyncio.run(app.run(host=HOST, port=PORT, debug=True))