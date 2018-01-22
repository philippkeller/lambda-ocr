import boto3
import tarfile
import os
import subprocess


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SCRIPT_DIR, 'lib')
DOWNLOAD_FILE = 'scan.tar.gz'
TMP_DIR = ''

s3 = boto3.client('s3')

def ocr(src_bucketname, src_filename, dest_bucketname):
	s3.download_file(src_bucketname, src_filename, "{}/{}".format(TMP_DIR, DOWNLOAD_FILE))
	tar = tarfile.open("{}/{}".format(SCRIPT_DIR, DOWNLOAD_FILE))
	tar.extractall(path=TMP_DIR)
	with open('{}/filenames.txt'.format(TMP_DIR), 'w') as f:
	    f.write("\n".join(tar.getnames()))
	env = os.environ.copy()
	env.update(dict(LD_LIBRARY_PATH=LIB_DIR, TESSDATA_PREFIX=SCRIPT_DIR))
	out = subprocess.check_output(['./tesseract', 
		'{}/filenames.txt'.format(TMP_DIR),
		'{}/out'.format(TMP_DIR),
		'pdf'], cwd=SCRIPT_DIR, env=env)
	print(out)
	for f in ['filenames.txt', DOWNLOAD_FILE] + tar.getnames():
		os.remove("{}/{}".format(TMP_DIR, f))