import tarfile
tf = tarfile.open('pyongwon.tar')
print(tarfile.is_tarfile('pyongwon.tar'))
tf.extractall()
