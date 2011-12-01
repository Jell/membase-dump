# Install:

    gem install membase-dump

# How to:

* Dump data:

    tap_dump localhost:11210 > dump.csv

The output is a tab separated csv with key, value encoded in base 64 and ttl.

* Load data:

    tap_load localhost:11234 < dump.csv

* Do it all in one step:

    tap_dump localhost:11210 | tap_load localhost:11234

# TODO:

* Make something less ugly
* Write some tests
* Rewrite the python code in ruby
