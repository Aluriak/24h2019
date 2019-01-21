


install_things:
	pip install -r requirements.txt
install_other_repos:
	mkdir -p other_repos
	cd other_repos && git clone https://github.com/haum/mqtt_mpd
	cd other_repos && git clone https://github.com/haum/laumio
	cd other_repos/mqtt_mpd && pip install -r requirements.txt


t: test
test:
	python -m pytest *.py -vv --ignore=venv --doctest-module


.PHONY: t test

listen_broadcast:
	mosquitto_sub -h localhost -t "#" -v

simul_atmos:
	mosquitto_pub -h localhost -m '1025' -t 'atmosphere/pression' -r
	mosquitto_pub -h localhost -m '25' -t 'atmosphere/temperature' -r
	mosquitto_pub -h localhost -m '50' -t 'atmosphere/humidite_absolue' -r
	mosquitto_pub -h localhost -m '65' -t 'atmosphere/humidite' -r

simul_distance:
	mosquitto_pub -h localhost -m '10' -t 'distance/value' -r
	
simul_red:
	mosquitto_pub -h localhost -m 'ON' -t 'capteur_bp/switch/led1/state' -r
	sleep 5
	mosquitto_pub -h localhost -m 'OFF' -t 'capteur_bp/switch/led1/state' -r

simul_announce:
	mosquitto_pub -h localhost -m 'Laumio_1D9486' -t 'laumio/status/advertise' -r
	mosquitto_pub -h localhost -m 'Laumio_104A13' -t 'laumio/status/advertise' -r

launch_mqtt_proxy:
	python ./mqtt_proxy.py

launch_domoticz:
	sudo service domoticz start
