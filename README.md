# SpacePlane
 1. The game is called SpacePlane which is using Pygame and Python.
 2. The plane can shoot bullets to destroy the meteorite to survive, otherwise it will loose the shield.

# Game Feature
  1. Show the shield volume of the space plane
  2. Show the score your space plane get so far
  3. Customize sounds and animation for things such like
        1. meteorite explosion
        2. bullet shoots
        3. plane explosion
  4. Three lives of the plane per game
  
  # Control the plane
  1. Using the left key or A key on the keyboard to move the plane turn left
  2. Using the right key or D key on the keyboard to move the plane turn right
  3. Using the up key or W key on the keyboard to move the plane turn up
  4. Using the down key or S key on the keyboard to move the plane turn down
  5. Using the space key on the keyboard to let the plane shoot bullets  
  6. Using the ESC key or Q key on the keyboard to quit the game           

# The Structure of ShootPlane:
  1. In this folder, the folder called assets is picture library
  2. In this folder, the folder called sounds is sound library
  3. In this folder, the document called shootPlane.py is the main programming code
  4. In this folder, the document called test.py is the test code which can print the remaining lives of the plane.
  
  The terminal can get the result:
    1. pygame 1.9.6
    2. Hello from the pygame community. https://www.pygame.org/contribute.html
    3. Enter the next page
    4. The initial lives of the plane are  3
    5. The plane is destroyed, the remaining lives are  2
    6. The plane is destroyed, the remaining lives are  1
    7. The plane is destroyed, the remaining lives are  0
    8. The live of plane is 0, so game over
    
# How to run the code:
   1. Create a virtual environment by running mkvirtualenv plane_env. DO NOT BUILD YOUR CODE TO YOUR SYSTEM'S PYTHON.
   2. Activate your new environment by running workon plane_env. If you use PyCharm, you should also change the interpreter to this virtual environment.
   3. In order to run the code, you should install pygame in your environment. Simply type "pip3 install pygame".
   4. Then, type "python3 shootPlane.py" to run the game
   5. Finally type "python3 test.py" to run the test code to get the above result in terminal
