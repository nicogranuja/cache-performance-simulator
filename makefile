default: trace1

trace1:
	@python3 main.py -f trace_files/Trace1.trc -s 1024 -b 16 -a 2 -r RR

tiny:
	@python3 main.py -f trace_files/Tiny.trc -s 1024 -b 16 -a 2 -r RR