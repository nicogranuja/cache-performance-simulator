#!/bin/bash

file=trace_files/A9.trc
# file=trace_files/Trace4.trc
s=1024
b=8
a=2
r=RR

# Default values
default_size=1024
default_block=8
default_a=2
default_r=RR

function cache_size_change() {
    echo -e "\n*** Running Cache Change ***\n"
    output_file="output/cache_changeZZZ.txt"
    echo "Start" > $output_file
    s=1
    
    while [[ s -lt 8193 ]];do
        echo "executing with params -f $file -s $s -b $b -a $a -r $r"
        ./sim.exe -f $file -s $s -b $b -a $a -r $r >> $output_file
        echo "BATCH END" >> $output_file
        
        s=$((2 * s))
    done

    # Reset
    s=1024
}

function block_size_change() {
    echo -e "\n*** Running Block Change ***\n"
    output_file="output/block_change.txt"
    echo "Start" > $output_file
    b=4
    
    while [[ b -lt 65 ]];do
        echo "executing with params -f $file -s $s -b $b -a $a -r $r"
        ./sim.exe -f $file -s $s -b $b -a $a -r $r >> $output_file
        echo "BATCH END" >> $output_file
        
        b=$((2 * b))
    done

    # Reset
    b=4
}

function associativity_size_change() {
    echo -e "\n*** Running Associativity Change ***\n"
    output_file="output/associativity_change.txt"
    echo "Start" > $output_file
    a=1
    
    while [[ a -lt 17 ]];do
        echo "executing with params -f $file -s $s -b $b -a $a -r $r"
        ./sim.exe -f $file -s $s -b $b -a $a -r $r >> $output_file
        echo "BATCH END" >> $output_file

        a=$((2 * a))
    done

    # Reset
    a=2
}

# cache_size_change
# block_size_change
# associativity_size_change