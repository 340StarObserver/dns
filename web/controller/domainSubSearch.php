<?php

// usage : deal request for query by a sub string of domain name

include_once("../model/elasticConn.php");
include_once("../model/domainQuery.php");


// first accept parameters
/*
	$fromid and $size 	: to provide page search
	$domainSub 		: a sub string of a domain name
	$date 			: like "20160603"
	$ismeta 		: whether search in metadata collection
*/
$fromid=(isset($_POST["fromid"])?intval($_POST["fromid"]):-1);
$size=(isset($_POST["size"])?intval($_POST["size"]):0);
$domainSub=(isset($_POST["domainSub"])?$_POST["domainSub"]:"");
$date=(isset($_POST["date"])?$_POST["date"]:null);
$ismeta=(isset($_POST["ismeta"])?intval($_POST["ismeta"]):0);


// example
/*
$fromid=0;
$size=3;
$domainSub="ucweb";
$date="20160626";
$ismeta=1;
*/


// then judge data format
$response='{}';
if($fromid>=0 && $size>0 && strlen($domainSub)>0 && $date!=null){

	// then do query
	$typestr="querydata";
	$term="question";
	if($ismeta==0){
		$typestr="dnsdata";
		$term="name";
	}
	$url="http://localhost:9200/dns".$date."/".$typestr."/_search";
	$json=domainSub($term,$fromid,$size,$domainSub);
	$es=getCurl();
	curl_setopt($es,CURLOPT_URL,$url);
	curl_setopt($es,CURLOPT_POST,1);
	curl_setopt($es,CURLOPT_POSTFIELDS,$json);
	try{
		$response=curl_exec($es);
	}catch(Exception $e){
	}finally{
		curl_close($es);
	}
}


// finally return the response
header("Content-Type:application/json;charset=utf-8");
echo $response;
