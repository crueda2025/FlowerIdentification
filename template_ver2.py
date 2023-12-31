import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import numpy as np
import sklearn
from sklearn.metrics import confusion_matrix

###########################MAGIC HAPPENS HERE##########################
# Change the hyper-parameters to get the model performs well
config = {
    'batch_size': 80,
    'image_size': (30,30),
    'epochs': 100,
    'optimizer': keras.optimizers.experimental.SGD(5e-3)
}
###########################MAGIC ENDS  HERE##########################

def read_data():
    train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
        "./images/flower_photos",
        validation_split=0.2,
        subset="both",
        seed=42,
        image_size=config['image_size'],
        batch_size=config['batch_size'],
        labels='inferred',
        label_mode = 'int'
    )
    val_batches = tf.data.experimental.cardinality(val_ds)
    test_ds = val_ds.take(val_batches // 2)
    val_ds = val_ds.skip(val_batches // 2)
    return train_ds, val_ds, test_ds

def data_processing(ds):
    data_augmentation = keras.Sequential(
        [
            ###########################MAGIC HAPPENS HERE##########################
            # Use dataset augmentation methods to prevent overfitting, 
            layers.RandomFlip("horizontal_and_vertical"),
            layers.RandomRotation(0.3),
            #layers.RandomContrast([.85, 1.15])
            ###########################MAGIC ENDS HERE##########################
        ]
    )
    ds = ds.map(
        lambda img, label: (data_augmentation(img), label),
        num_parallel_calls=tf.data.AUTOTUNE,
    )
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds

def build_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    x = layers.Rescaling(1./255)(inputs)
    ###########################MAGIC HAPPENS HERE##########################
    # Build up a neural network to achieve better performance.
    # Use Keras API like `x = layers.XXX()(x)`
    # Hint: Use a Deeper network (i.e., more hidden layers, different type of layers)
    # and different combination of activation function to achieve better result.
    hidden_units = 6
    hidden_layer_2 = 12
    hidden_layer_3 = 6
    x = layers.Flatten()(x)
    x = layers.Dense(hidden_units, activation='relu')(x)
    x = layers.Dense(hidden_layer_2, activation='relu')(x)
    x = layers.Dense(hidden_layer_3, activation='relu')(x)

    

    ###########################MAGIC ENDS HERE##########################
    outputs = layers.Dense(num_classes, activation="softmax", kernel_initializer='he_normal')(x)
    model = keras.Model(inputs, outputs)
    print(model.summary())
    return model



if __name__ == '__main__':
    # Load and Process the dataset
    train_ds, val_ds, test_ds = read_data()
    train_ds = data_processing(train_ds)
    # Build up the ANN model
    model = build_model(config['image_size']+(3,), 5)
    # Compile the model with optimizer and loss function
    model.compile(
        optimizer=config['optimizer'],
        loss='SparseCategoricalCrossentropy',
        metrics=["accuracy"],
    )
    # Fit the model with training dataset
    history = model.fit(
        train_ds,
        epochs=config['epochs'],
        validation_data=val_ds
    )
    ###########################MAGIC HAPPENS HERE##########################
    print(history.history)
    temp_history = history.history
    test_loss, test_acc = model.evaluate(test_ds, verbose=2)
    print("\nTest Accuracy: ", test_acc)
    test_images = np.concatenate([x for x, y in test_ds], axis=0)
    test_labels = np.concatenate([y for x, y in test_ds], axis=0)
    test_prediction = np.argmax(model.predict(test_images),1)
    # 1. Visualize the confusion matrix by matplotlib and sklearn based on test_prediction and test_labels
    # 2. Report the precision and recall for 10 different classes
    # Hint: check the precision and recall functions from sklearn package or you can implement these function by yourselves.
    # 3. Visualize three misclassified images
    # Hint: Use the test_images array to generate the misclassified images using matplotlib
    plt.plot(range(config['epochs']), temp_history["accuracy"], label = "Training")
    plt.plot(range(config['epochs']), temp_history["val_accuracy"], label = "Validation")
    plt.legend()
    plt.show()
    fig, ax = plt.subplots()
    # Here
    flowers = sklearn.metrics.confusion_matrix(test_labels, test_prediction)
    im = ax.imshow(flowers)



    ax.set_xticks(range(5))
    ax.set_yticks(range(5))

    plt.setp(ax.get_xticklabels(), rotation = 45, ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(5):
        for j in range(5):
            text = ax.text(j, i, flowers[i, j],
                        ha="center", va="center", color="w")

    ax.set_title("Confusion Matrix")
    fig.tight_layout()
    plt.show()




    ###########################MAGIC HAPPENS HERE##########################