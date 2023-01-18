import json
import base64
from algosdk import mnemonic, constants, transaction, mnemonic
from algosdk.v2client import algod


def make_transaction(private_key, my_address, message):

    #define the client
    algod_client = algod.AlgodClient(
        algod_token="",
        algod_address="https://testnet-algorand.api.purestake.io/ps2",
        headers={"X-API-Key": "WTKXJ8WsLa14pDEiXXJgt9EXRW7p0B8be3WSQfI1"}
    )

    print("My address: {}".format(my_address))
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE 
    params.fee = 1000
    receiver = '4O6BRAPVLX5ID23AZWV33TICD35TI6JWOHXVLPGO4VRJATO6MZZQRKC7RI'
    amount = 1420000
    note = message.encode()

    unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(private_key)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee) ) 


    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")


#Account A information
private_key_a = mnemonic.to_private_key("client zero color text meat typical extra fetch setup cradle wool sea dolphin strong ahead frame decorate solid mad minimum skull amount brick abandon gain")
account_a = '24TKEILVMFUMWMKT7LTHIEYTOG2IPT3MLTUFZISMJE3QI33PRU5EPKCC7U'

#Account B information
private_key_b = mnemonic.to_private_key("stay parade rack puzzle journey grace atom squeeze prefer shaft sail cactus kangaroo tenant knife mention brand anger differ night pride twist melt able carbon")
account_b = 'WXGQIUWJQP73Y62UXR5HXCB5ED5CN3B75VFPIKIEJSRVCOJ35MT6QUDWOQ'


#make the first transaction
make_transaction(private_key_a, account_a, 'my first Algorand transaction')

#make the second transaction
make_transaction(private_key_b, account_b, 'my second Algorand transaction')