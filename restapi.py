#!flask/bin/python
from flask import Flask, jsonify

from params import pool_fee
import wallet_json_rpc
import mining
import sqlite_handler

app = Flask(__name__)

@app.route('/pool_data', methods=['GET'])
def get_pool_data():
    network_height = wallet_json_rpc.get_current_block()
    pool_data = {
        "current_block": str(network_height),
        "net_hashrate": str(wallet_json_rpc.get_net_hashrate(network_height)) + " Gh",
        "algorithm": "Pascal",
        "poolhash": str(round(mining.get_pool_hr() / 10**9, 2)) + " Gh",
        "nethash":  0,
        "workers":  str(mining.No_miners()),
        "fee":      str(pool_fee) + "%",
        "period":   "Every block"
    }
    return jsonify({'pool_data': pool_data})

@app.route('/miner_data/<int:account>', methods=['GET'])
def get_miner_data(account):
    miner_data = {
        "account": str(account),
        "hashrate": str(round(mining.get_hr(account) / 10**9, 3)) + " Gh",
        "1hour":            0,
        "24hours":          0,
        "average_mined":    0,
        "payments":         sqlite_handler.db.get_account_payments(account)
    }
    return jsonify({'miner_data': miner_data})

def start_restapi():
    app.run(debug=False, port = 3000)
