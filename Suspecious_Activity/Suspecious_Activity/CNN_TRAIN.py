import warnings
warnings.filterwarnings('ignore') # suppress import warnings

import os
import cv2
import tflearn
import numpy as np
import tensorflow as tf
from random import shuffle
from tqdm import tqdm 
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

''' <global actions> '''

TRAIN_DIR = r'E:\Suspecious_Activity\Data'

#TEST_DIR = 'test/test'
IMG_SIZE = 50
LR = 1e-3
MODEL_NAME = 'VIOLENCE-{}-{}.model'.format(LR, '2conv-basic')
tf.logging.set_verbosity(tf.logging.ERROR) # suppress keep_dims warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # suppress tensorflow gpu logs
tf.reset_default_graph()

''' </global actions> '''

def label_leaves(lung):
    lungtype = lung[0]
    ans = [0,0,0,0]

    if lungtype == 'C': ans = [1,0,0,0]
    elif lungtype == 'F': ans = [0,1,0,0]
    elif lungtype == 'G': ans = [0,0,1,0]
    elif lungtype == 'K': ans = [0,0,0,1]

    return ans

def create_training_data():

    training_data = []

    for img in tqdm(os.listdir(TRAIN_DIR)):
        label = label_leaves(img)
        path = os.path.join(TRAIN_DIR,img)
        img = cv2.imread(path,cv2.IMREAD_COLOR)
        
        img = cv2.resize(img, (IMG_SIZE,IMG_SIZE), interpolation = cv2.INTER_AREA)
        
            
        training_data.append([np.array(img),np.array(label)])

    shuffle(training_data)
    np.save('train_data.npy', training_data)

    return training_data

def main():

    train_data = create_training_data()

    convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 3], name='input')

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 128, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = fully_connected(convnet, 1024, activation='relu')
    convnet = dropout(convnet, 0.8)

    convnet = fully_connected(convnet, 4, activation='softmax')
    convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(convnet, tensorboard_dir='log')


    if os.path.exists('{}.meta'.format(MODEL_NAME)):
        model.load(MODEL_NAME)
        print('Model Loaded')

    train = train_data[:1000]
    test = train_data[1000:]
    
    
    X = np.array([i[0] for i in train]).reshape(-1,IMG_SIZE,IMG_SIZE,3)

    Y = [i[1] for i in train]

    test_x = np.array([i[0] for i in test]).reshape(-1,IMG_SIZE,IMG_SIZE,3)
    test_y = [i[1] for i in test]
    model_info = model.fit({'input': X}, {'targets': Y}, n_epoch=30, validation_set=({'input': test_x}, {'targets': test_y}), snapshot_step=40, show_metric=True, run_id=MODEL_NAME)

    print(model_info)
    model.save(MODEL_NAME)
    

    

#    from sklearn.metrics import classification_report
#
#    pred = model.predict(test_x)
#
#    predicted = np.argmax(pred, axis=1)
#    report = classification_report(np.argmax(test_y, axis=1), predicted)
#    print(report)

    # # plot model history after each epoch
    # from plt_graph import plot_model_history
    # plot_model_history(model_info)
    #
    # return Str
if __name__ == '__main__':
    main()












#Importig the transfer learning model VGG19
from keras.applications import VGG19
    
# Assigning weight and input shape
model_sec=VGG19(weights="imagenet",include_top=False,input_shape=(224,224,3))
model_sec.summary()

# Generating the data
data_final = ImageDataGenerator(rescale = 1/255, zoom_range = 0.2,horizontal_flip=True,vertical_flip=True).flow_from_directory(path,target_size=(224,224),color_mode="rgb",classes=["Rifle","tank","guns","knife images"],batch_size=90)


# Making the strting top layers of the model as non-trainable
for layer in model_sec.layers:
    layer.trainable=False
    
model_2=model_sec.output

# Adding the last trainable layers to the model
model_2= Flatten()(model_2)
model_2= Dense(512,activation="relu")(model_2)
model_2= Dropout(0.3)(model_2)
model_2= Dense(256,activation="relu")(model_2)
model_2= Dropout(0.3)(model_2)
pred= Dense(4,activation="softmax")(model_2)
model_final =Model(input=model_sec.input,output=pred)


# Compiling the model
model_final.compile(loss="categorical_crossentropy",optimizer="adam",metrics=["accuracy"])


# Training
history = model_final.fit_generator(data_final,steps_per_epoch=int(1273/80),epochs=8,shuffle=False,callbacks=[clbk])


model_final.save("Myfinal_model_2.h5")


loss_final= history.history["loss"]
acc_final = history.history["acc"]

plt.plot(loss_final,color="r")
plt.title("Loss Progression Curve")



plt.plot(acc_final,color="b")
plt.title("Accuracy Progression Curve")


    