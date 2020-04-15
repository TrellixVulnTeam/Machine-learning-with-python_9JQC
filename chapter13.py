# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 11:34:34 2020

@author: Sima Soltani
"""

import tensorflow as tf
import numpy as np
np.set_printoptions(precision=3)

a= np.array([1,2,3],dtype=np.int32)
b = [4,5,6]

t_a=tf.convert_to_tensor(a)
t_b=tf.convert_to_tensor(b)

print(t_a)
print(t_b)

t_ones = tf.ones((2,3))
t_ones.shape
t_ones.numpy()

const_tensor = tf.constant([1.2,5,np.pi],dtype = tf.float32)
print(const_tensor)

t_a_new = tf.cast(t_a,tf.int64)
print(t_a_new.dtype)
t= tf.random.uniform(shape =(3,5))
t_tr  = tf.transpose(t)
print(t.shape,' --> ',t_tr.shape)

t = tf.zeros((30,))
t_reshape = tf.reshape (t,shape =(5,6))
print(t_reshape.shape)

t = tf.zeros((1,2,1,4,1))
t_sqz = tf.squeeze(t,axis=(2,4))
print(t.shape,'-->',t_sqz.shape)


tf.random.set_seed(1)
t1 = tf.random.uniform(shape =(5,2),minval =-1.0,maxval =1.0)
t2 = tf.random.normal(shape=(5,2),mean = 0.0, stddev= 1.0)

t3 = tf.multiply(t1,t2).numpy()
print (t3)
t4 = tf.math.reduce_mean(t3, axis=1)
print(t4)
t5 = tf.math.reduce_sum(t3, axis=1)
print(t5)
t6 = tf.linalg.matmul(t1,t2,transpose_b=True)
print(t6)
t7 = tf.linalg.matmul(t1,t2,transpose_a = True)
print(t7.numpy())
norm_t1 = tf.norm(t1,ord=2,axis =1).numpy()
print(norm_t1)

tf.random.set_seed(1)
t = tf.random.uniform((6,))
print(t.numpy())

t_splits = tf.split(t,num_or_size_splits=3)
[item.numpy() for item in t_splits]

tf.random.set_seed(1)
t = tf.random.uniform((5,))
print(t.numpy())
t_splits=tf.split(t,num_or_size_splits=[3,2])
[item.numpy() for item in t_splits]

A = tf.ones((3,))
B=tf.zeros((2,))
c = tf.concat([A,B],axis = 0)
print(c.numpy())

A = tf.ones((3,))
B = tf.zeros((3,))
C = tf.stack([A,B],axis=1)
print(C.numpy())


# Creating a Tensorflow Dataset from existing tensors

a = [1.2, 3.4, 7.5, 4.1, 5.0, 1.0]
ds = tf.data.Dataset.from_tensor_slices(a)
print(ds)
for item in ds:
    print(item)
    
# creat batches 
ds_batch = ds.batch(3)
for i , elem in enumerate(ds_batch,1):
    print('batch {}:'.format(i),elem.numpy())
    
# combining two tensors into a joint dataset
tf.random.set_seed(1)
t_x = tf.random.uniform([4,3],dtype=tf.float32)
t_y = tf.range(4)

ds_x = tf.data.Dataset.from_tensor_slices(t_x)
ds_y = tf.data.Dataset.from_tensor_slices(t_y)
ds_joint = tf.data.Dataset.zip((ds_x,ds_y))
for example in ds_joint:
    print(' x:', example[0].numpy(),
          ' y:',example[1].numpy())
    
ds_joint = tf.data.Dataset.from_tensor_slices((t_x,t_y))
for example in ds_joint:
    print(' x:',example[0].numpy(),
          ' y:', example[1].numpy())

#scale feature to the range of [-1,1)
ds_trans = ds_joint.map(lambda x,y: (x*2-1.0,y))
for example in ds_trans:
    print(' x:', example[0].numpy(),
          ' y:', example[1].numpy())
    
#  shuffle, batch , and repeat
tf.random.set_seed(1)
ds = ds_joint.shuffle(buffer_size = len(t_x))
for example in ds :
    print(' x:',  example[0].numpy(),
          ' y:', example[1].numpy())

ds = ds_joint.batch(batch_size = 3,
                    drop_remainder = False)
batch_x,batch_y = next(iter(ds))
print ('Batch-x:\n',batch_x.numpy())
print('Batch-y:\n',batch_y.numpy())

#repeat
ds = ds_joint.batch(3).repeat(count = 2)
for i ,(batch_x,batch_y) in enumerate(ds):
    print(i,batch_x.shape,batch_y.numpy())
    
ds = ds_joint.repeat(count=2).batch(3)
for i,(batch_x,batch_y) in enumerate(ds):
    print(i,batch_x.shape,batch_y.numpy())
    
## oder 1: Shuffle -> batch-> order
tf.random.set_seed(1)
ds=ds_joint.shuffle(4).batch(2).repeat(3)
for i,(batch_x,batch_y) in enumerate(ds):
    print(i,batch_x.shape,batch_y.numpy())
    
##order 2 : batch-->shuffle--repeat
tf.random.set_seed(1)
ds=ds_joint.batch(2).shuffle(4).repeat(3)
for i,(batch_x,batch_y) in enumerate(ds):
    print(i,batch_x.shape,batch_y.numpy())
    
# create dataset from files on your locla storage disk
import pathlib
imgdir_path = pathlib.Path('data\cat_dog_images')
file_list = sorted([str(path) for path in imgdir_path.glob('*.jpg')])

import matplotlib.pyplot as plt
import os

fig = plt.figure(figsize=(10,5))
for i,file in enumerate(file_list):
    img_raw = tf.io.read_file(file)
    img = tf.image.decode_image(img_raw)
    print('Image shape:', img.shape)
    ax = fig.add_subplot(2,3,i+1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.imshow(img)
    ax.set_title(os.path.basename(file),size = 15)
plt.tight_layout()
plt.show()

labels =[1 if 'dog' in os.path.basename(file) else 0 for file in file_list]
print(labels)

ds_files_labels = tf.data.Dataset.from_tensor_slices((file_list,labels))
for item in ds_files_labels:
    print(item[0].numpy(),item[1].numpy())
    
# function of preprocessing an image
def load_and_preprocess(path,label):
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image,channels=3)
    image = tf.image.resize(image, [img_height, img_width])
    image /=255.0
    return image,label

img_height,img_width = 80,120
ds_images_labels = ds_files_labels.map(load_and_preprocess)

fig = plt.figure(figsize = (10,6))
for i,example in enumerate(ds_images_labels):
    ax=fig.add_subplot(2,3,i+1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.imshow(example[0])
    ax.set_title('{}'.format(example[1].numpy()),
                 size = 15)
plt.tight_layout()
plt.show()

#fetching available datasets from the tensorflow_datasets libraray
import tensorflow_datasets as tfds
print(len(tfds.list_builders()))
print(tfds.list_builders())

# fetching dataset
#first approach:
    #1. calling the dataset builder function
    #2. Executing the download_and_prepare() metod
    #3. calling the as_dataset() method
celeba_bldr = tfds.builder('celeb_a')
print(celeba_bldr.info.features)
print(celeba_bldr.info.features['image'])
print(celeba_bldr.info.features['attributes'].keys())
print(celeba_bldr.info.citation)

celeba_bldr.download_and_prepare()
datasets = celeba_bldr.as_dataset(shuffle_files=False)
datasets.keys()

ds_train = datasets['train']
assert isinstance(ds_train,tf.data.Dataset)
example = next(iter(ds_train))
print(type(example))
print(example.keys())

ds_train = ds_train.map(lambda item:(item['image'],
                                     tf.cast(item['attributes']['Male'],
                                             tf.int32)))

ds_train = ds_train.batch(18)
images,labels = next(iter(ds_train))
print(images.shape,labels)
fig = plt.figure(figsize = (12,8))
for  i ,(image,label) in enumerate (zip(images,labels)):
    ax = fig.add_subplot(3,6,i+1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.imshow(image)
    ax.set_title('{}'.format(label),size=15)
plt.show()