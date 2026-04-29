# backend/services/blockchain.py
import hashlib, time, json
def blockchain_timestamp(report_dict):
    rec = json.dumps(report_dict, sort_keys=True)
    timestamp = str(time.time())
    hash_val = hashlib.sha256((rec + "|" + timestamp).encode()).hexdigest()
    return {"hash": hash_val, "timestamp": timestamp}
