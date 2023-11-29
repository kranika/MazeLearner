
# MazeLearner
A retro version of MazeRunner that utilises Python 3D modelling to expose a 'Word of the Day Challenge' in a maze. The player navigates within the maze, with the help of letters which will adapt a certain color, as the guide towards the end goal.


## Setting up the environment
* Clone the repository as shown:

`git@github.com:kranika/MazeLearner.git`
* Change to the project directory:

`cd MazeLearner`
* Required libraries and packages are listed in the `requirements.txt` file.

* To check/refresh the required modules for the project, run the following command on your project directory:

`pip freeze > requirements.txt`

* Install the required modules in the `requirements.txt` file by running the following command:

`pip install -r requirements.txt`

* Run the project by typing the following command:

`python main.py`
  (This instruction depends on how you run your .py files)

* Setting up personal logs

`import logging`
  
`logging.basicConfig(filename='log.txt', level=logging.INFO)`

  Learn more about [Python logs](https://docs.python.org/3/library/logging.html).
  

* You may need to obtain a **Wordnik API Key** in order to work with word meanings.

  Visit [Wordnik](https://developer.wordnik.com) to learn more.

## Contribution
Contributions are welcome! Feel free to submit bug reports, feature requests, or even pull requests to improve the game.

## License
This project is licensed under the [MIT License](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt).

