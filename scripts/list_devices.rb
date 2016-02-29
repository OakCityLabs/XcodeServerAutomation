#!/usr/bin/env ruby

require "spaceship"

Spaceship.login(ENV['DELIVER_USER'], ENV['DELIVER_PASSWORD'])

devices = Spaceship.device.all

for device in devices
    puts "#{device.udid}\t#{device.name}"
end


File.open('devices.txt', 'w') do |f|
    f.puts "Device ID\tDevice Name"
    devices.each do |device|
        f.puts "#{device.udid}\t#{device.name}"
    end
end 
