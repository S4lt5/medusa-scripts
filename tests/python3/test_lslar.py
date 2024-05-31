import pytest
from unittest.mock import patch
from . import medusa
import types
from scripts.lslar import lslar

#needed to monkey patch a new method type that works with "self"
medusa.lslar = types.MethodType(lslar,medusa)

    
def test_lslar():  
    print()         
    print(medusa.lslar("/usr/bin"))
