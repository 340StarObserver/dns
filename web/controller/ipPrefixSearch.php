<?php

// usage : deal request for query by a prefix string of ip

include_once("../model/elasticConn.php");
include_once("../model/ipQuery.php");


// first accept parameters
/*
	$fromid and $size 	: to provide page search
	$ipPrefix 		: a prefix string of a ip address
	$date 			: like "20160603"
	$term 			: "srcip" or "dstip"
*/
$fromid=(isset($_POST["fromid"])?intval($_POST["fromid"]):-1);
$size=(isset($_POST["size"])?intval($_POST["size"]):0);
$ipPrefix=(isset($_POST["ipPrefix"])?$_POST["ipPrefix"]:"");
$date=(isset($_POST["date"])?$_POST["date"]:null);
$term=(isset($_POST["term"])?$_POST["term"]:null);


// example
/*
$fromid=0;
$size=3;
$ipPrefix="158.169";
$date="20160626";
$term="dstip";
*/


// then judge data format
$response='{}';
if($fromid>=0 && $size>0 && strlen($ipPrefix)>0 && $date!=null && $term!=null){

	// then do query
	$url="http://localhost:9200/dns".$date."/querydata/_search";
	$json=ipQueryJson($term,$fromid,$size,$ipPrefix);
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
