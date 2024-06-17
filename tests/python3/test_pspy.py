import pytest
import subprocess
import types
from . import medusa
from scripts.pspy import pspy
#needed to monkey patch a new method type that works with "self"
medusa.pspy = types.MethodType(pspy,medusa)
   

def test_i_see_my_pids_i_create():      
    SLEEP_TIME = 11
    print(f"Sleeping {SLEEP_TIME}s, to see if I can catch new processes.")    
    subprocess.Popen(["sleep 1;for i in {1..10}; do ping 8.8.8.8 -c 1; sleep 1; done"],shell=True)        
    subprocess.Popen(["sleep 4 && cat /etc/hosts | base64"],shell=True)    
    new_pids = medusa.pspy(duration=SLEEP_TIME,sleep_time=0.0001)
    
    #if we have none.. I dunno what wacky environ we are in..
    assert len(new_pids) > 0
    found_ping = False
    found_hosts = False
    for pid in new_pids.split('\n'):
        print(pid)
        if "ping 8.8.8.8 -c 1" in pid:
            found_ping = "found_ping"
        if "sleep" in pid:
            found_hosts = "found_hosts"    
    #kinda silly, but helps output on pytest -v
    assert found_ping == "found_ping"
    assert found_hosts == "found_hosts"    
    


def test_safeguards():
    results = medusa.pspy(duration=-100)
    assert results == [("0","nope","nope")]

    results = medusa.pspy(duration=-600)
    assert results == [("0","nope","nope")]        


def test_stuff():
    assert True == True