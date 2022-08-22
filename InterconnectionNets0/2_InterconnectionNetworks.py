import tensorflow as tf
import tensorflow.keras as keras

# [1] @book{Geron19,
# author = "Geron, Aurelien",
# title = "Hands-On Machine Learning with
# Scikit-Learn, Keras, and TensorFlow - 2nd ed",
# publisher = "OReilly Media 2019",
# year = "2019"
# }
#
# [2] @book{Dally04,
# author = "Dally, William James  and  Towles,
# Brian Patrick",
# title = "Principles and Practices of
# Interconnection Networks - 1st Ed",
# publisher = "Morgan Kaufmann (2004)",
# year = "2004"
# }
#
# [3] @book{Thorpe84,
# author = "Thorpe, John A.  and  Kumpel, P.G.",
# title = "Elementary Linear Algebra",
# publisher = "Saunders College Publishing",
# year = "1984"
#}
#

# [2]:
# logic - transforms data and combines it
# memory - moves data in time
# communication - moves data in location

# [3] - transform basis vectors to new basis
# vectors

# [1] - learn patterns of (input,output) pairs

import numpy as np

def ei(i,n):
    I = np.identity(n,dtype=np.int8)
    e = I[i]
    e = e.reshape((n,1))
    e = np.matrix(e)
    return e
def eij(i,j,n):
    e = np.zeros((n,n),dtype=np.int8)
    e[j,i] = 1
    e = np.matrix(e)
    return e
def Transform1(A,x):
    y = A * x
    return y

n = 7
xa = ei(3,n)
print("xa = ",list(np.array(xa).flatten()))
A = eij(3,5,n)
print("A = \n",A)
yp = Transform1(A,xa)
print("yp = ",list(np.array(yp).flatten()))

def Transform_build(data,E=50): 
    N = len(data)
    X = []
    Y = []
    for tup in data:
        xx,yy = tup
        X.append(xx)
        Y.append(yy)
    n = len(X[0])
    m = len(Y[0])
    X = np.array(X)
    X = tf.constant(X)
    X = tf.reshape(X,[N,n,1])
    Y = np.array(Y)
    Y = np.array(Y)
    Y = tf.reshape(Y,[N,m,1])
    print("Building model...")
    model = keras.models.Sequential()
    model.add(keras.layers.InputLayer(
        input_shape=(X.shape[1:]),))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(100,
                activation='relu'))
    model.add(keras.layers.Dense(150,
                activation='relu'))
    model.add(keras.layers.Dense(m,
                activation='sigmoid'))
    loss0 = tf.keras.losses.BinaryCrossentropy()
    opt0 = tf.optimizers.RMSprop(0.001)
    model.compile(optimizer=opt0,
                loss=loss0)
    verbose0 = False
    print("Fitting data...please wait...")
    print("Training for E = ",E, "epochs")
    print("verbose = ", verbose0)
    model.fit(X,Y, epochs=E, verbose=verbose0)
    return model

def Transform(model):
    def f(x):
        n = len(x)
        x1 = tf.constant(np.array([x]))
        x1 = tf.reshape(x1,[1,n,1])
        yp = model(x1)
        yp = yp.numpy().flatten()
        yp2 = list(map(lambda x: int(round(x)),yp))
        return yp2
    return f

def fi(i,n):
    I = np.identity(n,dtype=np.int8)
    e = I[i]
    return e

n = 7
m = 8
data = [
    [fi(3,n),fi(5,m)],
    [fi(2,n),fi(3,m)+fi(2,m)],
    [fi(5,n),fi(1,m)+fi(0,m)+fi(4,m)],
    [fi(1,n)+fi(4,n), fi(6,m)]
    ]
model = Transform_build(data,E=50)
Transform2 = Transform(model)
for i in range(len(data)):
    tup = data[i]
    xa,ya = tup
    print('xa = ', list(xa.flatten()))
    print('ya = ', list(ya.flatten()))
    yp = Transform2(xa)
    print("yp = ", yp)
    print()
