from purse import Purse


purse = Purse(purse_url='http://localhost:3002', id=3)
print purse.create(name="wallet 3", force=True)
print purse.available_balance()
