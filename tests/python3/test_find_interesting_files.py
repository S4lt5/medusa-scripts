import pytest
from unittest.mock import patch
from . import medusa
import types
from scripts.find_interesting_files import find_interesting_files

#needed to monkey patch a new method type that works with "self"
medusa.find_interesting_files = types.MethodType(find_interesting_files,medusa)

    
def test_lslar():  
    print()         
    print(medusa.find_interesting_files("/usr/bin"))
