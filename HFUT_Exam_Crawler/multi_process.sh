#########################################################################
# File Name: multi_process.sh
# Author: Netcan
# Blog: http://www.netcan666.com
# mail: 1469709759@qq.com
# Created Time: 2016-06-18 六 19:45:32 CST
#########################################################################
#!/bin/bash

function multi_process {
	for i in {1..30}
	do
		php ./crawler.php &
	done
	wait
}

while :;
do
	multi_process
done
