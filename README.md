# python-seagate-flash-dump

Dumps Seagate HDD Flash memory using a serial connection and Python

** Use at your own risk **

## Instalation
`pip install -r requirements.txt`

## Running
`python dump_memory.py [start_address] [end_address]`

Address must be in `DEADBEEF`/`01234567` format.

ex: `python dump_memory.py 00001000 002c0000`

Memory will be dumped to a `.dump` file in the same directory.


