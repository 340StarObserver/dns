<?php

/*
provide a json for domain name query by a suffix string
	for example, domain is "w.seu.edu.cn", we hope to search by :
	"cn",
	"edu.cn",
	"seu.edu.cn",
	"w.seu.edu.cn"
parameters:
	$term 		: the name of term
	$fromid 	: from $fromid and size $size
	$size 		: from $fromid and size $size
	$domainSuffix 	: suffix string of a domain name
*/
function domainSuffix($term,$fromid,$size,$domainSuffix){
	$N=strlen($domainSuffix);
	if($domainSuffix[$N-1]!='.')
		$domainSuffix=$domainSuffix.'.';
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
					"term" : {
						'."\"".$term."\"".' : '."\"".$domainSuffix."\"".'
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


/*
provide a json for domain name query by a sub string
	for example, domain is "w.seu.edu.cn", we hope to search by :
	"www", "seu", "edu", "cn",
	"edu.cn", "seu.edu.cn", "www.seu.edu.cn"
parameters:
	$term 		: the name of term
	$fromid 	: from $fromid and size $size
	$size 		: from $fromid and size $size
	$domainSub 	: sub string of a domain name
*/
function domainSub($term,$fromid,$size,$domainSub){
	$N=strlen($domainSub);
	if($domainSub[$N-1]=='.')
		$domainSub=$domainSub.'*';
	else
		$domainSub=$domainSub.'.*';
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
							{"regexp":{'."\"".$term."\"".' : '."\"".$domainSub."\"".'}}
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
