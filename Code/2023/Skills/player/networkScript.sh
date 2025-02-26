hostname -I | awk '{
	for(i=1; i<=NF;i++){
		if(substr($i, 1, 3) == "172"){
			print($i)
		}
	}
}'
