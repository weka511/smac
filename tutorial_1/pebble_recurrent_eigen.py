import numpy

epsilon = 0.01
transfer = [[ epsilon, 1.0 - epsilon ],
            [ 1.0 - epsilon, epsilon ]]
eigenvalues, eigenvectors = numpy.linalg.eig(transfer)
print (eigenvalues)
 
# you may print the eigenvectors by uncommenting the following lines...
for iter in range(2):
   print (eigenvalues[iter])
   for i in range(2):
      print (eigenvectors[i][iter])

