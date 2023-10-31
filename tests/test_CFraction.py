from mathvis.cfractions import CFraction

def test_constructor():
    pass

def test_eq():
    pass

def test_neg_pos():
    pass

def test_addition():
    pass

def test_hash():
    assert hash(CFraction((1,2), 12)) == hash(complex(0.5, 12))

def test_division():
    cf = CFraction(21, -8) / CFraction(4,3)
    cm = complex(21, -8) / (4+3j)
    assert float(cf.real) == cm.real and float(cf.imag) == cm.imag

def test_complex_powers():
    pass

def test_negative_powers():
    pass

def test_rational_powers():
    assert CFraction(1)**0 == complex(1)**0
    assert CFraction(1)**8 == complex(1)**8
    assert CFraction(4)**6 == complex(4)**6
    assert float((CFraction(12)**-8).real) == complex(12)**-8
    cf = CFraction(12, -1)**-8
    cm = complex(12, -1)**-8
    assert float(cf.real) == cm.real and float(cf.imag) == cm.imag

    cf = CFraction(0, -8)**-7
    cm = complex(0, -8)**-7
    assert float(cf.real) == cm.real and float(cf.imag) == cm.imag

    cf = CFraction(19, 17)**12
    cm = complex(19, 17)**12
    assert float(cf.real) == cm.real and float(cf.imag) == cm.imag

def test_zero_powers():
    assert CFraction(0)**0 == 1
    assert CFraction(0)**1 == 0

    try:
        CFraction(0)**CFraction(-1,5j)
        assert False
    except:
        assert True

    try:
        CFraction(0)**(5+7j)
        assert False
    except:
        assert True

    try:
        CFraction(0)**-1
        assert False
    except:
        assert True

