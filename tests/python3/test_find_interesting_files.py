import pytest
from . import medusa
import types
from scripts.find_interesting_files import find_interesting_files

#needed to monkey patch a new method type that works with "self"
medusa.find_interesting_files = types.MethodType(find_interesting_files,medusa)
WRITABLE_BY_ALL = "*WRITABLE BY ALL"
WRITABLE_BY_USER = "*WRITABLE BY USER"  
WRITABLE_BY_GROUP = "*WRITABLE BY GROUP"  
SGID = "*SGID"
SUID = "*SUID"

ALL_TAGS = [
    WRITABLE_BY_ALL,
    WRITABLE_BY_USER,
    WRITABLE_BY_GROUP,
    SGID,
    SUID
]
    
def test_if_files_are_there():  
    output = medusa.find_interesting_files("/testfiles")

    expected_files = ["all.sh",
                      "group.sh","mine.sh",
                      "sgid.sh","suid.sh",
                      "777.txt"]
    
    for f in expected_files:
        assert f in output

def test_if_flags_work():  
    raw_output = medusa.find_interesting_files("/testfiles")
        
    #regular files should not show up
    assert ".hidden" not in raw_output
    assert "normal.sh" not in raw_output

    output = raw_output.split('\n')

    expected_files_and_tags = {"all.sh":[WRITABLE_BY_ALL],                      
                      "group.sh":[WRITABLE_BY_GROUP],
                      "mine.sh":[WRITABLE_BY_USER],
                      "normal.sh":[],
                      "sgid.sh":[SGID],
                      "suid.sh":[SUID],
                      "111.txt":[],
                      "777.txt":[WRITABLE_BY_ALL,WRITABLE_BY_GROUP,WRITABLE_BY_USER],                      
                      }    
        
    for filename in expected_files_and_tags.keys():
        found_match = False
        #for each key, comb the output for this file
        for line in output:            
            
            #this is slow, but whatver. Look for the line that mathces filename
            if filename in line:
                found_match = True
                #we found a match, so we're gonna check expected and unexpected tags for this file

                #get the tags we expect, as a list
                expected_tags = expected_files_and_tags[filename]
                for t in ALL_TAGS:
                    #check each tag, each time, positive and negative
                    if t in expected_tags:
                        #we expect this tag on this line.
                       
                        assert t in line                       
                    else:
                       
                        assert t not in line
    #if this fails, we missed a file
    assert found_match