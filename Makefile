


install_things:
	pip install -r requirements.txt
install_other_repos:
	mkdir -p other_repos
	cd other_repos && git clone https://github.com/haum/mqtt_mpd
	cd other_repos && git clone https://github.com/haum/laumio
	cd other_repos/mqtt_mpd && pip install -r requirements.txt
