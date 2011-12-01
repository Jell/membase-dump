require 'dalli'
require "base64"
require 'active_support'
require 'active_support/hash_with_indifferent_access'

module Membase
  module Dump
    def parse_mutation (line)
      key, base64_value, ttl = line.split
      raw_value = Base64.decode64(base64_value)
      raw = false
      value = begin
                Marshal.load(raw_value)
              rescue
                raw = true
                raw_value
              end
      [key, value, ttl, raw]
    end
  end
end
