#/bin/bash
fs='client.py worker.py crawl.py'
for f in $fs;do
	scp $f gm@gm141:~/text-classify/crawl
	scp $f gm@gm145:~/text-classify/crawl
done
