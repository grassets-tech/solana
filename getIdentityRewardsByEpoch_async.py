# usage: python3 getIdentityRewardsByEpoch_async.py --epoch 442 443 445 446 --identity <ID>
import asyncio
import aiohttp
import argparse
import requests
import logging
from string import Template
import json

endpoint = 'https://try-rpc.mainnet.solana.blockdaemon.tech'
EPOCH_SLOTS = 432000

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epoch',
        dest='epoch',
        nargs='+',
        required=True)
    parser.add_argument('--identity',
        dest='identity',
        type=str,
        required=True)
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
    response = requests.post(endpoint, json=json.loads(payload)).json()
    return response['result']

def GetRewardsFromBlock(block):
    rewards = 0
    # print(block)
    if block.get('error'):
        # print('Empty block')
        return 0
    transactions = block['result']['transactions']
    for t in transactions:
        rewards = rewards + int(t['meta']['fee'])
    return rewards/1E9/2

async def GetBlock(session, block_number, endpoint):
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

    async with session.post(endpoint, json=json.loads(payload)) as response:
        #print(await response.json())
        return await response.json()

def b(block_number, block):
    print(block)
    return (block_number, block)

async def runProgram(epoch, args):

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = []
        leader_schedule = GetLeaderSchedule(int(epoch)*EPOCH_SLOTS, args.identity, endpoint)
        for slot in leader_schedule[args.identity]:
            task = asyncio.ensure_future(GetBlock(session, int(epoch)*EPOCH_SLOTS+slot, endpoint))
            tasks.append(task)
        blocks = await asyncio.gather(*tasks)
    return(blocks)

def main():
    args = parseArguments() 
    for epoch in args.epoch:
        blocks = asyncio.run(runProgram(epoch, args))
        total_rewards = 0
        for b in blocks:
            rewards_block = GetRewardsFromBlock(b)
            # print('Rewards: {}'.format(rewards_block))
            total_rewards = total_rewards + rewards_block
        # print('='*20)
        print('Epoch: {}, Total Rewards: {}'.format(epoch, total_rewards))

if __name__ == "__main__":
    main()
