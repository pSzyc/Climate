from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
import tensorflow as tf
from keras import models, regularizers
from keras.layers import Dense, Dropout
import numpy as np



NGRAM_RANGE = (1, 3)

TOP_K = 7500

TOKEN_MODE = 'word'

MIN_DOCUMENT_FREQUENCY = 5

def ngram_vectorize(train_texts, train_labels, val_texts, return_models = False):

    kwargs = {
            'ngram_range': NGRAM_RANGE,
            'dtype': np.float32, 
            'strip_accents': 'unicode',
            'decode_error': 'replace',
            'analyzer': TOKEN_MODE, 
            'min_df': MIN_DOCUMENT_FREQUENCY,
    }
    vectorizer = TfidfVectorizer(**kwargs)

    x_train = vectorizer.fit_transform(train_texts)

    x_val = vectorizer.transform(val_texts)

    selector = SelectKBest(f_classif, k=min(TOP_K, x_train.shape[1]))
    selector.fit(x_train, train_labels)
    x_train = selector.transform(x_train).astype(np.float32)
    x_val = selector.transform(x_val).astype(np.float32)

    x_train = x_train.toarray()
    x_val = x_val.toarray()

    if return_models:
        return  x_train, x_val, vectorizer, selector
    else:
        return x_train, x_val

def vectorize(data, vectorizer, selector):
    data = vectorizer.transform(data)
    data = selector.transform(data).astype(np.float32)
    return data.toarray()


def _get_last_layer_units_and_activation(num_classes):
    if num_classes == 2:
        activation = 'sigmoid'
        units = 1
    else:
        activation = 'softmax'
        units = num_classes
    return units, activation

    

def mlp_model(layers, units, dropout_rate, input_shape, num_classes):
    op_units, op_activation = _get_last_layer_units_and_activation(num_classes)
    model = models.Sequential()
    model.add(Dense(units=units, activation='tanh', kernel_regularizer=regularizers.l2(0.01), input_shape=input_shape))

    for i in range(1, layers):
        model.add(Dropout(rate=dropout_rate))
        model.add(Dense(units=units/(2**i), activation='tanh', kernel_regularizer=regularizers.l2(0.01)))

    model.add(Dense(units=op_units, activation=op_activation))
    return model


def train_ngram_model(x_train, x_val, train_labels, val_labels, learning_rate=1e-3, epochs=1000, batch_size=128, layers=3, units=64, dropout_rate=0.3, num_classes = 2):
    
    # Create model instance.
    model = mlp_model(layers=layers,
                                  units=units,
                                  dropout_rate=dropout_rate,
                                  input_shape=x_train.shape[1:],
                                  num_classes=num_classes)

    # Compile model with learning parameters.
    if num_classes == 2:
        loss = 'binary_crossentropy'
    else:
        loss = 'sparse_categorical_crossentropy'
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss=loss, metrics=['acc'])

    # Create callback for early stopping on validation loss. If the loss does
    # not decrease in two consecutive tries, stop training.
    callbacks = [tf.keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=2)]

    # Train and validate model.
    history = model.fit(
            x_train,
            train_labels,
            epochs=epochs,
            callbacks=callbacks,
            validation_data=(x_val, val_labels),
            verbose=2,  # Logs once per epoch.
            batch_size=batch_size)

    # Print results.
    history = history.history
    return (history['val_acc'][-1], model)