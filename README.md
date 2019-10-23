# BooleanGenerator

Requires Python 3.7+.

Selectively uses `multiprocessing` to allow for longer computes to occur off GUI 
process, avoiding `tkinter` GUI locking up.

Currently in the process of reworking the `run.py` file to allow for better 
packaging as a windows executable.

Considering making the loading bar on long computes determinate i.e. shows you 
how far through generating the search it is, but since `tkinter` objects are not 
pikleable, it would be a fair bit of work beyond the scope of usage. 