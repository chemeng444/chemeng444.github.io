export name=Exercise_3_Transition_States
export header=_header.txt
for cluster in cees sherlock
do
	mkdir $name
	cp *py $name/
	## scripts to need header
	for script in fbl.py neb.py neb_restart.py run_freq.py
	do
		rm $name/$script
		cat ../../Scripts/$cluster$header $script >> $name/$script
	done
	chmod +x $name/*py
	tar -cvf exercise_3_$cluster.tar $name
	rm -r $name
done