import subprocess
import os
import time
tmpdir = os.getenv('TMP', "/tmp")

dbhost = "172.17.0.2"
dbname = "postgres"
dbuser = "postgres"
dbpass = "admin123"
dbport = 5432

dbset('db','pg')
dbset('bm','TPC-C')
dbset( 'vindex', 'hnsw')

diset('connection','pg_host', dbhost)
diset('connection','pg_port', dbport)
diset('connection','pg_sslmode','prefer')

diset('tpcc','pg_superuser', dbuser)
diset('tpcc','pg_superuserpass', dbpass)
diset('tpcc','pg_defaultdbase', dbname)
diset('tpcc','pg_user', dbuser)
diset('tpcc','pg_pass', dbpass)
diset('tpcc','pg_dbase', dbname )
diset('tpcc','pg_driver','timed')
diset('tpcc','pg_total_iterations','10000000')
diset('tpcc','pg_rampup','1')
diset('tpcc','pg_duration','1')
diset('tpcc','pg_allwarehouse','false')
diset('tpcc','pg_timeprofile','true')
diset('tpcc','pg_vacuum','false')
giset("commandline", "keepalive_margin", "90")

print("STARTED LOADING VECTOR DATA IN DB AND BUILDING INDEX")
result = subprocess.run(["vectordbbench", "pgvectorhnsw", "--config-file", "/home/emumba/emumba/VDB/VectorDBBench/vectordb_bench/config-files/sample_config.yml"], capture_output=True)
print(result)
print("VECTOR DATA LOADED AND INDEX BUILD COMPLETE")

if result.returncode == 0:
    buildschema()
    loadscript()
    vudestroy()
    print("TEST STARTED")
    vuset('vu','4')
    vucreate()
    tcstart()
    tcstatus()
    jobid = tclpy.eval('vurun')
    vudestroy()
    tcstop()
    print("TEST COMPLETE")
    file_path = os.path.join(tmpdir , "pg_tprocc" )
    fd = open(file_path, "w")
    fd.write(jobid)
    fd.close()
    time.sleep(10)

    print("STARTING RECALL CALCULATION")
    diset('tpcc','pg_driver','test')
    customscript("recall_calculation.tcl")
    vuset("vu", "1")
    vucreate()
    tcstart()
    tcstatus()
    jobid = tclpy.eval('vurun')
    vudestroy()
    tcstop()
    print("TEST COMPLETE")
    # TODO: Fix - logs are not being written to file
    file_path = os.path.join(tmpdir , "pg_tprocc" )
    fd = open(file_path, "w")
    fd.write(jobid)
    fd.close()
    print("RECALL CALUCLATION COMPLETE")
exit()