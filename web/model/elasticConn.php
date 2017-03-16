<?php

// get an object of curl
function getCurl(){
	$es=curl_init();
	curl_setopt($es,CURLOPT_RETURNTRANSFER,1);
	return $es;
}
