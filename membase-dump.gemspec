# -*- encoding: utf-8 -*-
$:.push File.expand_path("../lib", __FILE__)
require "membase-dump/version"

Gem::Specification.new do |s|
  s.name        = "membase-dump"
  s.version     = Membase::Dump::VERSION
  s.platform    = Gem::Platform::RUBY
  s.authors     = ["Jean-Louis Giordano"]
  s.email       = ["jean-louis@releware.com"]
  s.homepage    = ""
  s.summary     = %q{Compilation of scripts to make and load membase dumps through the Tap interface.}
  s.description = %q{Compilation of scripts to make and load membase dumps through the Tap interface.}

  s.rubyforge_project = "membase-dump"

  s.files         = `git ls-files`.split("\n")
  s.test_files    = `git ls-files -- {test,spec,features}/*`.split("\n")
  s.executables   = `git ls-files -- bin/*`.split("\n").map{ |f| File.basename(f) }
  s.require_paths = ["lib"]
  s.add_dependency("dalli")
  s.add_dependency("active_support")
  s.add_development_dependency("rake", "0.8.7")
end
