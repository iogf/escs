from cspkg.plugins.normal_mode import Normal, NormalMode
from cspkg.plugins.run_process import RunProcess
from subprocess import Popen, PIPE
import shlex

from cspkg.start import root
from cspkg.core import rcmod
import unittest

class TestRunProcess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rcmod.extend(((RunProcess, (), {}), (NormalMode, (), {})))

    @classmethod
    def tearDownClass(cls):
        root.destroy()

    def test0(self):
        """
        """
        xstr = root.note.create('Tests')
        root.note.select(xstr.master.master.master)
        xstr.focus_set()
        root.update() 

        xstr.event_generate('<Key-M>')
        root.update()

        scan = root.focus_get()
        scan.insert('end', 'ls')
        scan.event_generate('<Return>')
        root.update()

        data0 = xstr.get('1.0', 'end')
        process = Popen('ls', stdout=PIPE, stderr=PIPE, 
        text=True, shell=True)
        output, err = process.communicate()
        self.assertTrue(output in data0)

if __name__ == '__main__':
    unittest.main()
