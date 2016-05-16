# Elasticsearch

## Setup
Intall on Mac

	brew install elasticsearch
	ln -sfv /usr/local/opt/elasticsearch/*.plist ~/Library/LaunchAgents
	launchctl load ~/Library/LaunchAgents/homebrew.mxcl.elasticsearch.plist

Test

	curl -XGET http://localhost:9200/
