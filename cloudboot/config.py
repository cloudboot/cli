ROOT_DIR = '/home/lpsandaruwan/Desktop/cloudboot/temp'
SRC_DIR = '/'.join([ROOT_DIR, 'src'])
CACHE_DIR = '/'.join([ROOT_DIR, '.cloudboot_'])


cloud_functions_runtimes = ['nodejs', 'python', 'java', 'go']
cloud_functions_triggers = ['https', 'pubsub', 'storage', 'firestore']


def reset_root(path='.'):
    global ROOT_DIR, SRC_DIR, CACHE_DIR
    ROOT_DIR = path
    SRC_DIR = '/'.join([ROOT_DIR, '.cloudboot_'])
    CACHE_DIR = '/'.join([ROOT_DIR, '.cloudboot_'])
