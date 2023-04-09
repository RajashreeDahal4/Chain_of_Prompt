import pickle

def load_pickle_files(filepath,filename):
    with open(filepath + filename,'rb') as f:
        loaded_file = pickle.load(f)
    return loaded_file