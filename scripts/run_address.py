from cardano_wrapper.utils import Timer
from cardano_wrapper.wrappers.AddressWrap import AddressWrap

address = AddressWrap()
with Timer() as timer:
    print(address.generate(5))
print(str(timer.interval))