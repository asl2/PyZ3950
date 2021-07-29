import re
from PyZ3950 import ccl

def test_word():
    word_re = re.compile('^' + ccl.t_WORD + '$')
    # test initials
    assert word_re.match('a')
    assert word_re.match('Z')
    assert word_re.match('9')
    assert word_re.match('3')
    assert word_re.match(':')
    assert word_re.match('&')
    assert not word_re.match('!')
    
    # test noninitials
    # match literal '.' as a noninitial
    assert word_re.match('a.')
    # match literal "'" as a noninitial
    assert word_re.match("a'")
    # match literal ',' as a noninitial
    assert word_re.match('a,')
    # do not match '!' as a noninitial
    assert not word_re.match("a!")
    # match stuff allowed as an initial as noninitial
    assert word_re.match('a&')
    mo = word_re.match('a!')

    
    
    
