from test_base import ChainSyncBaseTestCase

from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter


class ChainSyncGetTransactionsTestCase(ChainSyncBaseTestCase):

    def setUp(self):
        adapter = SteemAdapter(
            endpoints='https://steemd.pevo.science',
            retry=False
        )
        self.chainsync = ChainSync(adapter=adapter, retry=False)

    def test_get_ops_in_transactions(self):
        blocks = [
            20905050,
            20905025,
        ]
        txs = [
            'a3815d4a17f1331481ec6bf89ba0844ce16175bc',
            'c68435a34a7afc701771eb090f96526ed4c2a37b',
        ]
        result = self.chainsync.get_ops_in_transactions(txs)
        for op in result:
            self.assertTrue(op['block_num'] in blocks)

    def test_get_ops_in_transactions_exception_no_transaction_id(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_transactions()

    def test_get_ops_in_transactions_exception_invalid_transaction_id(self):
        with self.assertRaises(Exception) as context:
            txs = [
                'a3815d4a17f1331481ec6bf89ba0844ce16175bc',
                '0000000000000000000000000000000000000000',  # invalid tx
            ]
            results = [op in self.chainsync.get_ops_in_transactions(txs)]
