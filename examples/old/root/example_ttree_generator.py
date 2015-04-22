# You need ROOT installed on your machine, and need to install pyroot, via ```pip install pyroot```

def generate_root_file_with_tree(self, file_name, mode="update"):

        f = root_open(file_name, mode)
        trees = ["Table 1", "Table 2", "Table 3"]

        for tree_name in trees:

            tree = Tree(name=tree_name,
            title=tree_name)
            # F - Float, I - Integer
            tree.create_branches(
            {'W_in_GEV_low': 'F',
            'W_in_GEV_high': 'F',
            'SIG_IN_NB_(<0.8)_ystatminus': 'F',
            'SIG_IN_NB_(<0.8)_ystat': 'F',
                 'SIG_IN_NB_(<0.8)_ystatplus': 'F',
                 'SIG_IN_NB_(<0.6)_ystatminus': 'F',
                 'SIG_IN_NB_(<0.6)_ystat': 'F',
                 'SIG_IN_NB_(<0.6)_ystatplus': 'F',
                   'i': 'I'})

            for i in xrange(10000):
                tree['W_in_GEV_low'] = gauss(1., 4.)
                tree['W_in_GEV_high'] = gauss(.3, 2.)
                tree['SIG_IN_NB_(<0.8)_ystatminus'] = gauss(0., 0.1)
                tree['SIG_IN_NB_(<0.8)_ystat'] = gauss(0., 5.)
                tree['SIG_IN_NB_(<0.8)_ystatplus'] = gauss(0., 0.1)
                tree['SIG_IN_NB_(<0.6)_ystatminus'] = gauss(0., 0.1)
                tree['SIG_IN_NB_(<0.6)_ystat'] = gauss(0., 5.)
                tree['SIG_IN_NB_(<0.6)_ystatplus'] = gauss(0., 0.1)
                tree.i = i
                tree.fill()

            tree.write()

        f.close()