const API_URL = "https://eth-goerli.g.alchemy.com/v2/[Your api key here]"  // TODO
const PUBLIC_KEY = "[Your account address here]"; // TODO 
const PRIVATE_KEY = "[Your private key here]"; // TODO

const { createAlchemyWeb3 } = require("@alch/alchemy-web3")
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

  let hashOfName = "[SHA-256 hash of your name]"; // TODO

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
    data: "" //TODO add a call to mintNFT here
  }

  await sendTx(tx2);

}

mintNFT()
