from pydano.utils import Timer
from pydano.wrappers.AddressWrap import AddressWrap

address = AddressWrap("../my-config.yaml")
with Timer() as timer:
    print(address.generate(addresses=5, wallet_type="byron"))
print(str(timer.interval))
