import os, shutil


class preprocessor:
    def __init__(self):
        self.data = True

    def prepare_output_dir(self):
        # Check for tmp project directory.
        # If directory already exists then
        # - remove already existing files.
        if os.path.exists('/tmp/ryu/'):
            print '[+] /tmp/ryu/ path exists.'
            print '[+] Deleting /tmp/ryu'
            shutil.rmtree('/tmp/ryu')
        print '[+] Creating /tmp/ryu/'
        try:
            os.mkdir('/tmp/ryu/')
        except:
            print '[-] Oops! Exception occurred.'
            return False
        print '[+] /tmp/ryu/ - Created successfully'

