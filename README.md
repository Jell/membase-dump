# Install:

    gem install bundler -v=1.0.11
    bundle install

# How to:

* Dump data:

    ./tap_dump.py localhost:11210 | sort | uniq > dump.csv

The output is a tab separated csv with key, value encoded in base 64 and ttl.

* Load data:

    ./load_tap_dump.rb localhost:11234 < dump.csv

* Do it all in one step:

    ./tap_dump.py localhost:11210 | sort | uniq | ./load_tap_dump.rb localhost:11234

# TODO:

* Rewrite the python code in ruby
* Make a gem out of it
