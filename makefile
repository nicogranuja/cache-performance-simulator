default: trace1

trace1:
	@echo "8 offset"
	@python3 main.py -f trace_files/trace1.trc -s 1024 -b 8 -a 2 -r RR
	@echo "4 offset"
	@python3 main.py -f trace_files/trace1.trc -s 1024 -b 4 -a 2 -r RR

win-trace1:
	@echo "8 offset"
	@wine CacheSim.exe -f trace_files/trace1.trc -s 1024 -b 8 -a 2 -r RR
	@echo "4 offset"
	@wine CacheSim.exe -f trace_files/trace1.trc -s 1024 -b 4 -a 2 -r RR

trace1-copy:
	# @echo "8 offset"
	# @python3 main.py -f trace_files/trace1-copy.trc -s 1024 -b 8 -a 2 -r RR
	@echo "4 offset"
	@python3 main.py -f trace_files/trace1-copy.trc -s 1024 -b 4 -a 2 -r RR

win-trace1-copy:
	# @echo "8 offset"
	# @wine CacheSim.exe -f trace_files/trace1-copy.trc -s 1024 -b 8 -a 2 -r RR
	@echo "4 offset"
	@wine CacheSim.exe -f trace_files/trace1-copy.trc -s 1024 -b 4 -a 2 -r RR -log test

tiny:
	@python3 main.py -f trace_files/Tiny.trc -s 1024 -b 4 -a 2 -r RR

win-tiny:
	@wine CacheSim.exe -f trace_files/Tiny.trc -s 1024 -b 4 -a 2 -r RR

A9:
	@python3 main.py -f trace_files/A9.trc -s 1024 -b 4 -a 2 -r RR

win-A9:
	@wine CacheSim.exe -f trace_files/A9.trc -s 1024 -b 4 -a 2 -r RR