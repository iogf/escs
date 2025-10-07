from cspkg.core import EscsApp

import unittest

class TestEscsApp(unittest.TestCase):
    def setUp(self):
        self.root = EscsApp()
        # self.root = tk.Tk()
        # self.app = App(self.root)

    def tearDown(self):
        self.root.destroy()

    def test0(self):
        self.assertEqual()
        # self.app.button.invoke() 
        # self.root.update_idletasks()

if __name__ == '__main__':
    unittest.main()

