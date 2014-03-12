import requests
from decimal import Decimal


class Purse(object):

    purse_url = None

    def __init__(self, purse_url=None, id=None):
        self.purse_url = purse_url
        self.id = id

        self.name = None
        self.description = None

    def __repr__(self):
        return "<Purse %s:%s:%s>" % (self.id, self.name, self.description)

    def _url(self, endpoint):
        return "%s/%s" % (self.purse_url, endpoint)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'available_balance': str(self.available_balance),
        }

    def create(self, name=None, description=None, force=False):
        """
        Creates a new purse.
        """
        # Don't create a wallet if id is set unless force
        # is set to true.
        if self.id and not force:
            return False

        data = {
            'wallet[id]': self.id,
            'wallet[name]': name,
            'wallet[description]': description,
        }

        r = requests.post(self._url('wallets'), data=data)
        data = r.json()

        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        return self

    def get_wallet(self, id):
        return Purse(purse_url=self.purse_url, id=id)

    def _set_properties(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @property
    def exists(self):
        """
        Checks if the wallet exists
        """
        r = requests.get(self._url('wallets/%s.json' % self.id))
        self._set_properties(**r.json())
        return r.status_code == 200

    @property
    def available_balance(self):
        """
        Gets the available balance.
        """
        r = requests.get(self._url('wallets/%s/balance' % self.id))
        return Decimal(r.json().get('balance'))

    def topup(self, amount, expiry=None):
        """
        Adds balance to the current purse.
        """
        data = {
            'amount': amount
        }
        r = requests.post(self._url('wallets/%s/topup' % self.id), data=data)
        return Decimal(r.json().get('balance'))

    def charge(self, amount, expiry=None):
        """
        Deducts balance to the current purse.
        """
        raise NotImplementedError

    def transfer(self, amount, receiving_id):
        """
        Transfers balance to another purse.
        """
        raise NotImplementedError

    def reserve(self, amount):
        """
        Reserves an amount from the current purse.
        """
        raise NotImplementedError

    def cancel(self, reference_id):
        """
        Cancels a reservation.
        """
        raise NotImplementedError

    def complete(self, reference_id):
        """
        Completes a reservation.
        """
        raise NotImplementedError
