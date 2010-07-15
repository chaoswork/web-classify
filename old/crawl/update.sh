#/bin/bash
fs='client/client.py worker/worker.py config.py client/task1.py worker/parser.py worker/job.py util.py'
hosts='gm141 gm145'
dirname=/home/gm/text-classify/crawl

for host in $hosts;do
	for f in $fs;do
		scp $f gm@$host:$dirname
	done
	ssh gm@$host "rm -r $dirname/pages"
done

rm -r /home/xh/mp/text-classify/crawl/pages

