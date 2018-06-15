import json
import time
import requests
import datetime

import os
from os import sys, path
import django

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qobit_cms.settings")
django.setup()

from general.models import *
from utils import send_email

def main():
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    coins = requests.get(url).json().get('Data', {})

    all_coins = {}
    for coin in CryptocompareCoin.objects.filter(is_deleted=False):
        all_coins[coin.symbol] = coin.id

    for key, val in coins.items():
        if val.get('Symbol') in all_coins:
            all_coins.pop(val.get('Symbol'))

        defaults = {
            'name': val.get('Name'),
            'coinname': val.get('CoinName'),
            'fullname': val.get('FullName'),
            'image_uri': val.get('ImageUrl'),
            "is_deleted": False
        }

        coin, is_new = CryptocompareCoin.objects.update_or_create(symbol=val.get('Symbol'), defaults=defaults)
        # if is_new:
        #     send_email(val.get('Symbol'), True, 'Cryptocompare')

        # mcoin = MasterCoin.objects.filter(cryptocompare=coin.id).first()
        # if mcoin:
        #     url_ = 'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={}'.format(val['Id'])
        #     info = requests.get(url_).json()['Data']['General']

        #     launch_date = datetime.datetime.strptime(info['StartDate'], '%d/%m/%Y') if info.get('StartDate') and info.get('StartDate') != '01/01/0001' else None

        #     defaults = {
        #         'website_url': info.get('WebsiteUrl'),
        #         'launch_date': launch_date,
        #         'algorithm': info.get('Algorithm'),
        #         'twitter_handle': info.get('Twitter'),
        #         'proof_type': info.get('ProofType'),
        #         'block_time': info.get('BlockTime') or -1,
        #         'block_reward': info.get('BlockReward')
        #     }

    if all_coins:
        CryptocompareCoin.objects.filter(id__in=all_coins.values()).update(is_deleted=True)


if __name__ == "__main__":
    main()