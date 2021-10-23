# NFT_Monitor
This is a telegram bot for monitoring price and ranking of NFT on Binance Smart Chain.

Can fetch latest ranking and price in real time.
- ``/Pancake_NFT/nft-web3.py``: Main file to fetch transaction and log through web3.
- ``/Pancake_NFT/pancake_nft.py``: Original version to fetch log from bscscan. Now aborted.

## 0x00 Requirement

Available for Python3.8+, recommend to use `virtualenv` to run this project.

- python-telegram-bot==13.7
- web3==5.24.0

## 0x01 Usage

- Modify configuration in `config.py`
  - `TEST_BOT_TOKEN` : tgbot token of test environment
  - `PROD_BOT_TOKEN`: tgbot token of produce environment
  - `COLLECTION_CONTRACT_ADDRESS`: NFT Collection Contract
  - `CONTRACT_ADDRESS`:  Contract address of market place

Now, default value is fetch from `PancakeSwapSquad` NFT.

- Run it, recommend deploy it on server

  ```
  python crypto_bot.py
  ```

- Input command in bot

  ```
  /nft [MAXIMUM_RANKING] [MAXIMUM_PRICE] 
  
  eg: /nft 5000 5
  ```

## 0x02 Interface 

![image-20211023162759858](https://cdn.jsdelivr.net/gh/pyf0311/myPrivateIMGBed/markdown/1634978029980.png)

## 0x03 Rewards
If u think this project is helpful, would u like to buy me a cup of coffee?
- ERC-20 & BEP-20: 0x2733c1818Bc39639808ba35688177ec0DD97D520
