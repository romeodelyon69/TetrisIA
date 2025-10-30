This code provide a DQN agent to play a basic version of the game TETRIS using TensorFlow.

If you want to train a new model : run neuralNetwork.py

If you want to test this model : run runModel.py

If you simply want to play the game : run main.py

Controls : Left and right arrow allow you to move a piece (right and left) while the up arrow allows you to rotate the piece. 

How does it works : when a new piece arrives, the AI computes all the possible places where it could land and use a trained neural network to give a score to each of them. Then it simply choose the move with the
highest score associated. 

For the training, the idea is to explore random move while playing more and more with the insight the model has learned. The model bases itslef on some feature of the game like the number of holes in the grid, the 
height of the highest tower, the gaps between consecutive columns and son one to predict a score for a given grid. 

Because it plays less and less randomly you should see the maximum socre rapidly increase when reaching 2000 epochs (the moment the model completly stops to explore random branches). 
