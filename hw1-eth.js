const API_URL = "https://eth-goerli.g.alchemy.com/v2/0FtJhESkXxCpmahbhYqn_kl7T5Du4QUP"  // TODO
const PUBLIC_KEY = "0x0A160de5C1bD37560A29E00e778bBD255Ead9573"; // TODO 
const PRIVATE_KEY = "c188ea59bc5fc1c51ffd3067f844cfef6773e744dde03fa3aa72daee26abd43d"; // TODO

const { createAlchemyWeb3 } = require("@alch/alchemy-web3");
const { dir } = require("console");
const web3 = createAlchemyWeb3(API_URL)

const contract = require("./IntroToBlockchainNFT.json")
const contractAddress = "0x978A328Cc24C0b50a0D9F97787938E67CF09F9A9"
const nftContract = new web3.eth.Contract(contract.abi, contractAddress)


async function sendTx(tx) {
    const signPromise = web3.eth.accounts.signTransaction(tx, PRIVATE_KEY);
    signPromise.then((signedTx) => {
          web3.eth.sendSignedTransaction(
            signedTx.rawTransaction,
            function (err, hash) {
              if (!err) {
                console.log("The hash of your transaction is: ", hash)
              } else {
                console.log("Something went wrong when submitting your transaction:", err)
              }
            }
          )
        }).catch((err) => {
          console.log("Promise failed:", err)
    })
}

async function mintNFT(tokenURI) {

  let hashOfName = "306364168740ac3852ce7405fd3a2ab3965bd66a9d52f177ab9da1117421582a"; // TODO

  let nonce = await web3.eth.getTransactionCount(PUBLIC_KEY, "latest") //get latest nonce

  const tx1 = {
    from: PUBLIC_KEY,
    to: contractAddress,
    nonce: nonce,
    gas: 500000,
    data: nftContract.methods.enterAddressIntoBook(hashOfName).encodeABI()
  }

  await sendTx(tx1);

  nonce += 1; 

  const tx2 = {
    from: PUBLIC_KEY,
    to: contractAddress,
    nonce: nonce,
    gas: 500000,
    data: nftContract.methods.mintNFT().encodeABI()
  }

  await sendTx(tx2);

}

mintNFT()
