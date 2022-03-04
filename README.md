# Effective Frontier

This library is made to help you estimate the perfect investment portfolio depending on historical data. 
The data is currently fetched from [poloniex](https://poloniex.com/) which has only crypto data.\

It can now also work with stocks. 

## Installation

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install the following libraries:

```bash
pip3 install pandas
pip3 install numpy
pip3 install request
pip3 install matplotlib

```

## Usage
The script is called with asset pairs as arguments. If the assets are cryptocurrencies then they have to be exactly as in [poloniex](https://poloniex.com/).
```bash
python3 EffectiveFrontier <coin_pair1 coin_pair2 coin_pair3 ....>
```
i.e.
```bash
python3 EffectiveFrontier USDT_BTC USDT_ETH USDT_MATIC
python3 EffectiveFrontier AMZN TSLA 
```

## Result


```bash
USDT_BTC:24.78%
USDT_ETH:23.02%
USDT_MATIC:37.61%
USDT_LINK:14.59%
```
![alt text](https://github.com/AabedSolayman/EffectiveFrontier/blob/images/Figure_1.png?raw=true)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
