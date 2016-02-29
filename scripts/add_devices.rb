#!/usr/bin/env ruby

require "spaceship"

Spaceship.login(ENV['DELIVER_USER'], ENV['DELIVER_PASSWORD'])

unless ARGV.length == 1
  puts "Dude, not the right number of arguments."
  puts "Usage: add_devices.rb device-udid-export.txt\n"
  exit
end

filename = ARGV[0]

file = File.new(filename, "r")
while (line = file.gets)
    fields = line.split()
    if fields[0].length != 40
        next
    end
    udid = fields.shift
    name = fields.join(" ")
    puts "Register device => Name: >#{name}< UDID: >#{udid}<"
    Spaceship.device.create!(name: name, udid: udid)
end
file.close

##########################################################
# Update all adhoc profiles to contain the new devices.
##########################################################

profiles = Spaceship.provisioning_profile.ad_hoc.all

for profile in profiles
    # Add all available devices to the profile
    profile.devices = Spaceship.device.all
    # Push the changes back to the Apple Developer Portal
    profile.update!
end
