#!/usr/bin/env python3

import argparse
import requests
import logging
from string import Template
import json

endpoint = 'https://try-rpc.mainnet.solana.blockdaemon.tech'
block_number = 192888028
EPOCH_SLOTS = 432000

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epoch',
        dest='epoch',
        nargs='+')
    parser.add_argument('--identity',
        dest='identity',
        type=str)
    return parser.parse_args()

def GetLeaderSchedule(slot_number, identity, endpoint):
    t = Template(""" 
    { 
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getLeaderSchedule",
        "params": [
        $slot,
        {
            "identity": "$identity"
        }
    ] }
    """)
    payload = t.substitute(slot=slot_number, identity=identity)
    #print(payload)
    try:
        response = requests.post(endpoint, json=json.loads(payload)).json()
    except requests.exceptions.RequestException as e:
        logging.error('Check connection {}'.format(e))
        sys.exit()
    if response.get('error'):
        logging.error('Check endpoint {}'.format(response))
        sys.exit()
    if not response.get('result'):
        logging.error('Can\'t get {}'.format(response))
        sys.exit()
    #print(response)
    return response['result']  

def GetBlock(block_number, endpoint):
    t = Template(""" 
    {
        "jsonrpc": "2.0",
        "id":1,
        "method":"getBlock",
        "params": [
        $block_number,
        {
            "encoding": "json",
            "maxSupportedTransactionVersion":0,
            "transactionDetails":"full"
        }
    ]}
    """)
    payload = t.substitute(block_number=block_number)
    #print(payload)
    #print(type(payload))
    try:
        response = requests.post(endpoint, json=json.loads(payload)).json()
    except requests.exceptions.RequestException as e:
        logging.error('Check connection {}'.format(e))
        sys.exit()
    if response.get('error'):
        logging.error('Check endpoint {}'.format(response))
        return
    if not response.get('result'):
        logging.error('Can\'t get {}'.format(response))
        sys.exit()
    # print(response)
    return response['result']['transactions']

def GetRewardsFromBlock(block):
    rewards = 0
    for t in block:
        rewards = rewards + int(t['meta']['fee'])
    return rewards/1E9/2

def main():
    args = parseArguments()
    for epoch in args.epoch:
        print('Epoch: {}'.format(epoch))
        print('='*20)
        leader_schedule = GetLeaderSchedule(int(epoch)*EPOCH_SLOTS, args.identity, endpoint)
        total_rewards = 0
        for slot in leader_schedule[args.identity]:
            block = GetBlock(int(epoch)*EPOCH_SLOTS+slot, endpoint)
            if block is None:
                rewards_block = 0
            else:
                rewards_block = GetRewardsFromBlock(block)
            print('Slot: {}, Rewards: {} SOL'.format(int(epoch)*EPOCH_SLOTS+slot, rewards_block))
            total_rewards = total_rewards + rewards_block
        print('='*20)
        print('Total Slots: '.format(len(leader_schedule[args.identity])))
        print('Total Rewards: {} SOL'.format(total_rewards))
        print('\n')       

if __name__ == "__main__":
    main()
