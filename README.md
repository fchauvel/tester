# SensApp::Tester

Runs integration tests against the SensApp architecture

# Installation

SensApp::Tester is a Python application that test whether the SensApp
architecture is up and running. Install it as follows:

	$ git clone http://github.com/fchauvel/tester.git
	$ cd tester
	$ pip install -r requirements.txt
	$ pip install .

Alternatively, you may use `pip install -e .` to install it in a
developper mode.

# Running

To check whether the SensApp architecture is up and running, we need a
bunch of sensors that push data to the SensApp::Receiver
service. Let's describe them into a YAML, as follows:

	# File data/sensor.yml
	sensors:

	  test1:
		id: 666
		description: A simple test sensor, that pretends to be registered
		unit: km/h
		period: 2
		data: [666, 666, 666]

	  test2:
		description: Another test sensor
		unit: cm
		period: 4
		data: [1, 3, 5, 7, 9, 11]

	  test3:
		description: Yet another test sensor
		unit: m
		period: 3
		data: [2, 4, 6, 8, 10]


Note that when sensors are given an identifier (field `id`), they will
not be registered.

It loads the sensors from the YAML file. Then it call the
SensApp::Registry to registers them and then starts a thread for each
sensor. Each thread starts to push data. When all are done, it reaches
out to the storage DB to check that all data have been stored (only
for the sensors that have been registered).

Here is an example run using the YAML above. No data coming from
Sensor `test1` is not stored, because it is not registered to the
Registry as he already have an identifier, but one that the Registry
does not know.


	$> sensapp-tester -s data/sensors.yml
	SensApp::Tester v0.0.0 (MIT)
	Copyright (C) 2018 SINTEF

	1. LOADING SENSORS (from 'data/sensors.yml')

	2. REGISTERING SENSORS:
		Sensor    ID
		test2    73
		test3    74

	3. PUSHING DATA:
		Sensor Action                        
		 test1 Started!                      
		 test2 Started!                      
		 test3 Started!                      
		 test1 Pushing value '666'           
		 test2 Pushing value '1'             
		 test3 Pushing value '2'             
		 test1 Pushing value '666'           
		 test3 Pushing value '4'             
		 test2 Pushing value '3'             
		 test1 Pushing value '666'           
		 test3 Pushing value '6'             
		 test1 Shutting down!                
		 test2 Pushing value '5'             
		 test3 Pushing value '8'             
		 test2 Pushing value '7'             
		 test3 Pushing value '10'            
		 test3 Shutting down!                
		 test2 Pushing value '9'             
		 test2 Pushing value '11'            
		 test2 Shutting down!                

	3. VERDICT (DB check):
		Sensor      Registered      Found   Expected  Verdict
		 test1           False          0          0     PASS
		 test2            True          6          6     PASS
		 test3            True          5          5     PASS

	That's all folks!

