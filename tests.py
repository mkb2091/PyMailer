'''
Test whether PyMailer does what it should
'''
import unittest
import PyMailer


class PyMailerTest(unittest.TestCase):
    '''PyMailer testing class '''
    def test_mxlookup(self):
        '''Test whether mxlookup returns expected output'''
        self.assertEqual(PyMailer.mxlookup('gmail.com'),
                         'gmail-smtp-in.l.google.com')

if __name__ == '__main__':
    unittest.main()
