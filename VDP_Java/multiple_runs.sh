#sleep 10m
for i in {1..4}
do
	python vuldeepecker.py prospector.txt 
	#>> out.txt
	sleep 2m
done