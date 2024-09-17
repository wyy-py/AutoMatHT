#!/bin/bash
#
# Prepare PBS file using available node and CPUs
#
# Written BY QIN, Guangzhao <qin.phys@gmail.com>
# 2023-12-20

# Define nodes to exclude
EXCLUDE_NODES=("node011" "node012" "node013" "node014" "node015" "node016")

_freenodes()
{
    pbsnodes -a | grep -E 'vnode|ncpus' | cut -d = -f 2 |\
    while read LINE
    do
        NCPUS_AVAILABLE=$LINE
        read NAME
        read NCPUS_ASSIGNED  

        echo "$NAME $NCPUS_AVAILABLE $NCPUS_ASSIGNED"
    done | tail -n +2 | sort -g -k 1 | tr -s ' ' '\n' |\
    while read LINE
    do
        # for each node
        NAME=$LINE
        read NCPUS_AVAILABLE
        read NCPUS_ASSIGNED
        NCPUS_FREE=$(($NCPUS_AVAILABLE - $NCPUS_ASSIGNED))

        # Check if the node is in the exclude list
        EXCLUDE=0
        for EXCLUDE_NODE in "${EXCLUDE_NODES[@]}"
        do
            if [ "$NAME" == "$EXCLUDE_NODE" ]; then
                EXCLUDE=1
                break
            fi
        done

        if [ $EXCLUDE -eq 1 ]; then
            continue
        fi

        # ---------------------

        if [ x"$NCPUS_FREE" != x0 ];then
            echo "nodes=$NAME:ppn=$NCPUS_FREE"
        fi
    done 
}

NodeINFO="$(_freenodes | head -1)"

echo '>> ' $NodeINFO
_freenodes | tail -n +2 | sed -e 's/^/    /g'

if [ x"$NodeINFO" == x ];then
    echo '>> No available node and CPU'
    exit
fi

touch AutoSubmit.pbs
cat >|AutoSubmit.pbs <<FILEEND
#!/bin/bash
#PBS -N AutoVASP
#PBS -l $NodeINFO
#PBS -q et
#PBS -j oe

EXE='/public/bin/ShengBTE-v1.1.1'
OUT=LOG.vasp

sleep 10s;exit

NPROCS=\$(wc -l < "\$PBS_NODEFILE")
cd "\$PBS_O_WORKDIR"
mpirun -machinefile "\$PBS_NODEFILE" -np \$NPROCS \$EXE >|\$OUT 2>&1

/public/bin/info_job.sh
FILEEND
