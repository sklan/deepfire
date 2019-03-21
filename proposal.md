# DeepFire
## Rapping Neural Networks on Android

## Introduction
Humans depend a lot on context. You don't start thinking from scratch each second. For example, suppose you are watching a movie. Your understanding of any scene depends upon whatever occurred in the past scenes. Gradually, you build up a complete understanding of the movie.

Traditional neural networks are unable to model this kind of learning. They are extremely constrained. They take fixed-sized inputs and give out fixed sized output. This is a glaring limitation when dealing with sequential data.

Recurrent neural networks model the sequential learning paradigm quite well. Their chain-like nature builds on earlier information to predict the future. 

Our project involves generating rap lyrics using character level RNNs. We plan to collect rap songs of various artists. For each artist, we will train a separate model. These models will then be served through an Android app.


## Breaking it Down
1. Collection and cleaning of songs
    - This involves collecting lyrics of multiple rappers 
    - Frameworks/Libraries: Pandas, Numpy, Scrapy
2. Training multiple character-level RNN/LSTM/GRU models
    - We will have to train a separate model for each of rapper we choose to add in our app.
    - Frameworks/Libraries: Keras, TensorFlow
3. Serving the models through an Android App
    - Depending what is more feasible we will either serve the model as a TFLite model or through a server.
    - Frameworks/Libraries: TensorFlow Lite, MLKit
    
