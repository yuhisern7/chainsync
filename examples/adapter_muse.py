import datetime

from chainsync import ChainSync
from chainsync.adapters.muse import MuseAdapter

adapter = MuseAdapter(endpoints=['http://45.79.206.79:8090/'], debug=False)
chainsync = ChainSync(adapter)

print('\nGetting block 1')
block = chainsync.get_block(1)
print(block)

print('\nGetting blocks 1, 10, 50, 250, 500')
blocks = chainsync.get_blocks([1, 10, 50, 250, 500])
for block in blocks:
    print(block)

print('\nGetting blocks 1000-1005')
blocks = chainsync.get_block_sequence(1000, 5)
for block in blocks:
    print(block)

print('\nGetting all ops in block 6274087...')
for op in chainsync.get_ops_in_block(6274087):
    print("{}: {} [{}] - {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type']))

print('\nGetting withdraw_vesting ops in block 6274087...')
for op in chainsync.get_ops_in_block(6274087, whitelist=['feed_publish']):
    print("{}: {} [{}] - {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type']))

print('\nGetting all ops in block 1000000, 5000000, and 2000000...')
for op in chainsync.get_ops_in_blocks([1000000, 5000000, 2000000]):
	print("{}: {} [{}] - {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type']))

print('\nGetting producer_reward ops in block 1000000, 5000000, and 2000000...')
for op in chainsync.get_ops_in_blocks([1000000, 5000000, 2000000], whitelist=['producer_reward']):
	print("{}: {} [{}] - {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type']))

print('\nStreaming blocks, 100 at a time, from the irreversible height...')
for dataType, block in chainsync.stream(['blocks'], batch_size=100, mode='irreversible'):
    print("{}: {} - {}".format(datetime.datetime.now(), block['block_num'], block['witness']))

print('\nStreaming all ops...')
for dataType, op in chainsync.stream(['ops']):
    print("{}: {} [{}] - {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type']))

print('\nStreaming all non-virtual ops...')
for dataType, op in chainsync.stream(['ops'], virtual_ops=False):
    print("{}: {} [{}] - {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type']))

print('\nStreaming all virtual ops...')
for dataType, op in chainsync.stream(['ops'], regular_ops=False):
    print("{}: {} [{}] - {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type']))

print('\nStreaming vote ops only...')
for dataType, op in chainsync.stream(['ops'], whitelist=['vote']):
    print("{}: {} - {} by {}".format(datetime.datetime.now(), op['block_num'], op['operation_type'], op['voter']))

print('\nStreaming producer_reward virtual ops only...')
for dataType, op in chainsync.stream(['ops'], whitelist=['producer_reward']):
    print("{}: {} - {} for {} of {}".format(datetime.datetime.now(), op['block_num'], op['operation_type'], op['producer'], op['vesting_shares']))

print('\nStreaming all blocks + ops + virtual ops + accurate counts of ops per block...')
for dataType, data in chainsync.stream(['blocks', 'ops', 'ops_per_blocks']):
    dataHeader = "{} #{}: {}".format(datetime.datetime.now(), data['block_num'], dataType)
    if dataType == "op":
        print("{} {} {}".format(dataHeader, data['transaction_id'], data['operation_type']))
    if dataType == "block":
        txCount = len(data['transactions'])
        opCount = sum([len(tx['operations']) for tx in data['transactions']])
        print("{} - #{} - tx: {} / ops: {}".format(dataHeader, data['block_num'], txCount, opCount))
    if dataType == "ops_per_blocks":
        for height in data:
            print("{} - #{}: {}".format(dataHeader, height, data[height]))

print('\nStreaming all blocks + ops (no virtual ops)...')
for dataType, data in chainsync.stream(['blocks', 'ops'], virtual_ops=False):
    dataHeader = "{}: {}".format(datetime.datetime.now(), dataType)
    if dataType == "op":
        print("{} {} {}".format(dataHeader, data['transaction_id'], data['operation_type']))
    if dataType == "block":
        txCount = len(data['transactions'])
        opCount = sum([len(tx['operations']) for tx in data['transactions']])
        print("{} - tx: {} / ops: {}".format(dataHeader, txCount, opCount))

print('\nStreaming all blocks + ops (no virtual ops), filtering only votes...')
for dataType, data in chainsync.stream(['blocks', 'ops'], whitelist=['vote'], virtual_ops=False):
    dataHeader = "{}: {}".format(datetime.datetime.now(), dataType)
    if dataType == "op":
        print("{} {} {}".format(dataHeader, data['transaction_id'], data['operation_type']))
    if dataType == "block":
        txCount = len(data['transactions'])
        opCount = sum([len(tx['operations']) for tx in data['transactions']])
        print("{} - tx: {} / ops: {}".format(dataHeader, txCount, opCount))

print('\nStreaming all blocks + virtual ops (no normal ops)...')
for dataType, data in chainsync.stream(['blocks', 'ops'], regular_ops=False):
    dataHeader = "{}: {}".format(datetime.datetime.now(), dataType)
    if dataType == "op":
        print("{} {} {}".format(dataHeader, data['transaction_id'], data['operation_type']))
    if dataType == "block":
        txCount = len(data['transactions'])
        opCount = sum([len(tx['operations']) for tx in data['transactions']])
        print("{} - tx: {} / ops: {}".format(dataHeader, txCount, opCount))

print('\nStreaming all blocks + virtual ops (no normal ops), filtering only producer_reward...')
for dataType, data in chainsync.stream(['blocks', 'ops'], regular_ops=False, whitelist=['producer_reward']):
    dataHeader = "{}: {}".format(datetime.datetime.now(), dataType)
    if dataType == "op":
        print("{} {} {}".format(dataHeader, data['transaction_id'], data['operation_type']))
    if dataType == "block":
        txCount = len(data['transactions'])
        opCount = sum([len(tx['operations']) for tx in data['transactions']])
        print("{} - tx: {} / ops: {}".format(dataHeader, txCount, opCount))
