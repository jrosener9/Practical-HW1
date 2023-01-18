
import json
import base64
from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
from algosdk.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
from algosdk.transaction import *


#account A information
private_key_a = mnemonic.to_private_key("client zero color text meat typical extra fetch setup cradle wool sea dolphin strong ahead frame decorate solid mad minimum skull amount brick abandon gain")
account_a = '24TKEILVMFUMWMKT7LTHIEYTOG2IPT3MLTUFZISMJE3QI33PRU5EPKCC7U'

#account B information
private_key_b = mnemonic.to_private_key("stay parade rack puzzle journey grace atom squeeze prefer shaft sail cactus kangaroo tenant knife mention brand anger differ night pride twist melt able carbon")
account_b = 'WXGQIUWJQP73Y62UXR5HXCB5ED5CN3B75VFPIKIEJSRVCOJ35MT6QUDWOQ'


#define the client
algod_client = algod.AlgodClient(
    algod_token="",
    algod_address="https://testnet-algorand.api.purestake.io/ps2",
    headers={"X-API-Key": "WTKXJ8WsLa14pDEiXXJgt9EXRW7p0B8be3WSQfI1"}
)

#----------------------------CREATE ASSET----------------------------
# Get network params for transactions before every transaction.
params = algod_client.suggested_params()

# Asset Creation transaction
txn = AssetConfigTxn(
    sender=account_a,
    sp=params,
    total=100,
    default_frozen=False,
    unit_name="JACK",
    asset_name="jack",
    manager=account_a,
    reserve=account_a,
    freeze=account_a,
    clawback=account_a,
    url="https://jack/details", 
    decimals=0)
# Sign with secret key of creator
stxn = txn.sign(private_key_a)
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))   
except Exception as err:
    print(err)
# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.
print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))



#----------------------------OPT-IN----------------------------


asset_id = 154572742

params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
params.fee = 1000
params.flat_fee = True

account_info = algod_client.account_info(account_b)
holding = None
idx = 0
for my_account_info in account_info['assets']:
    scrutinized_asset = account_info['assets'][idx]
    idx = idx + 1    
    if (scrutinized_asset['asset-id'] == asset_id):
        holding = True
        break

if not holding:
    
    # Use the AssetTransferTxn class to transfer assets and opt-in
    txn = AssetTransferTxn(
        sender=account_b,
        sp=params,
        receiver=account_b,
        amt=0,
        index=asset_id)
    stxn = txn.sign(private_key_b)
    txid = algod_client.send_transaction(stxn)
    print(txid)
    # Wait for the transaction to be confirmed
    wait_for_confirmation(algod_client, txid)



#----------------------------Transfer----------------------------

# transfer asset of 1 from account A to account B
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
params.fee = 1000
params.flat_fee = True
txn = AssetTransferTxn(
    sender=account_a,
    sp=params,
    receiver=account_b,
    amt=1,
    index=asset_id)
stxn = txn.sign(private_key_a)
txid = algod_client.send_transaction(stxn)
print(txid)
# Wait for the transaction to be confirmed
wait_for_confirmation(algod_client, txid)



#---------------------------- Atomic Transfer----------------------------

# build first transaction of payment from B to A
params = algod_client.suggested_params()
params.flat_fee = constants.MIN_TXN_FEE 
params.fee = 1000
receiver = account_a
amount = 1200000
note = "Sending to account A".encode()
txn_1 = transaction.PaymentTxn(account_b, params, receiver, amount, None, note)


# build second transaction of asset from A to B
txn_2 = AssetTransferTxn(
    sender=account_a,
    sp=params,
    receiver=account_b,
    amt=1,
    index=asset_id)


# get group id and assign it to transactions
gid = transaction.calculate_group_id([txn_1, txn_2])
txn_1.group = gid
txn_2.group = gid

# sign transactions
stxn_1 = txn_1.sign(private_key_b)    
stxn_2 = txn_2.sign(private_key_a)

#create group
signed_group =  [stxn_1, stxn_2]

#send transaction group
tx_id = algod_client.send_transactions(signed_group)

# wait for confirmation
confirmed_txn = wait_for_confirmation(algod_client, tx_id, 4)
print("txID: {}".format(tx_id), " confirmed in round: {}".format(
confirmed_txn.get("confirmed-round", 0))) 
