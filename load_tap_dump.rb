#! /usr/bin/env ruby
# encoding: ASCII-8BIT

require 'rubygems'
require 'bundler/setup'
require 'dalli'
require "base64"
require 'active_support'
require 'active_support/hash_with_indifferent_access'

client = Dalli::Client.new(ARGV.first)

while line = STDIN.gets
  key, base64_value, ttl = line.split
  raw_value = Base64.decode64(base64_value)
  raw = false
  value = begin
            Marshal.load(raw_value)
          rescue
            raw = true
            raw_value
          end
  puts "Set #{key} to #{value.inspect} with #{ttl} ttl #{raw ? '(raw)' : ''}"
  client.set(key, value, ttl.to_i, raw: raw)
end
