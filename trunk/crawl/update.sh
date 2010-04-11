#/bin/bash
fs='client.py worker.py config.py task1.py parser.py job.py util.py'
hosts='gm141 gm145'
dirname=/home/gm/text-classify/crawl

for host in $hosts;do
	for f in $fs;do
		scp $f gm@$host:$dirname
	done
	ssh gm@$host "rm -r $dirname/pages"
done

rm -r /home/xh/mp/text-classify/crawl/pages

