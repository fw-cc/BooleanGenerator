# BooleanGenerator

Requires Python 3.7+ (I love me a good `asyncio.create_task(coro)`), PIL.

Built to help generating "Must match n" boolean searches.

Pretty much everything has tooltips to explain usage.

Run `run.py`, it has a first-time-setup where it installs all dependencies it can (and updates `pip`).

`tkinter` on the top, `asyncio` most of the way through, `itertools` at the bottom.

Shouldn't break in normal operation (but then again, neither should fighter plane flight computers), if it does, hit the handy refresh 
button and let me know about the issue.

~~Gets a bit slow (and sort of breaks) when you reach 15-20 lines territory and 
decide it's a good idea to generate a query (that even takes `itertools` a second),
producing well over 60,000 characters in a woefully underbuilt `tkinter.ttk.Entry` that was never made 
for such a task. You should never need to run such a search, even if this worked, I'm 
sure that LinkedIn would break when you tried to paste it.~~ Fixed with latest dev patch.