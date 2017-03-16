<?php

/*
provide a json for ip query
	for example, ip is 11.22.33.44, we hope to search by :
	11
	11.22
	11.22.33
	11.22.33.44
parameters :
	$term 		: 	"srcip" or "dstip"
	$fromid 	: 	from $fromid and size $size
	$size 		: 	from $fromid and size $size
	$ipPrefix 	: 	prefix string of a ip address
*/
function ipQueryJson($term,$fromid,$size,$ipPrefix){
	$N=strlen($ipPrefix);
	if($ipPrefix[$N-1]=='.')
		$ipPrefix=$ipPrefix."*";
	else
		$ipPrefix=$ipPrefix.".*";
	$json='{
		"size" : '.$size.',
		"query" : {
			"filtered" : {
				"filter" : {
					"range" : {
						"pagingid" : {"gt":'.$fromid.'}
					}
				},
				"query" : {
					"bool" : {
						"must" : [
							{"regexp":{'."\"".$term."\"".' : '."\"".$ipPrefix."\"".'}}
						]
					}
				}
			}
		},
		"sort" : [
			{"pagingid":{"order":"asc"}}
		]
	}';
	return $json;
}
