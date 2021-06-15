from pydano.utils import Timer
from pydano.wrappers.AddressWrap import AddressWrap

address = AddressWrap()
with Timer() as timer:
    print(address.generate(5))
print(str(timer.interval))