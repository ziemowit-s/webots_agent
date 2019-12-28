Webots agent for Renforcement Learning

# Prerequisites
1. Install spikeagents library from the spiking_neural_agents GitHub repo:
    ```bash
    pip install git+https://github.com/ziemowit-s/spiking_neural_agents.git
    ```

2. Download stable Webots release: https://github.com/cyberbotics/webots/releases
3. Install Webots
4. Add to .bashrc:
    ```bash
    export WEBOTS_HOME="/usr/local/webots"
    export LD_LIBRARY_PATH="$WEBOTS_HOME/lib/controller"
    export PYTHONPATH="$WEBOTS_HOME/lib/controller/python36:$PYTHONPATH"
    ```

# How to work with Webots
You can deploy Python code for a robot controller directly from the IDE.
Each robot has its own controller file which is deployed 
by run button from IDE or from the console (by `python controller_name.py`).

You can load robot's controller directly to Webots, but probably your conda env and external libs won't work.

#### Running Webots  
  1. Type `webots` from the console

  2. To start project in Webots:
        * click Wizard
        * New Project Directory [Next] 
        * choose location [Next] 
        * name of your world file (with *.wbt extention) 
        * click "Add a rectangle area" [Next]
        * Finish 
  
  3.  To add new object (box, robots):
        * click + sign
        * click PROTO nodes (Webots Projects)
        * to add robot click "robots" and choose one for you
        * gctronic->epuck-EPuck (Robot) is a robot with camera view
  
#### To deploy code from PyCharm
  1. in Webots window select your robot on the node list
        * double click on the robot list element
        * click "controller"
        * click Select
        * choose "<Extern>"
  2. In PyCharm
        * run ide from console write `pycharm-profesional` or `pycharm-community `in the console.
          This will use all environmental variable from your .bashrc
        * select run.py file and click run button
        * open Webots window and click run
  3. This procedure run the code to the first robot which has \<extern> controller
  4. If you have more robots with \<extern> controller - go to Webots docs and find how to run them

# Run
1. Run Webots and open simulation/worlds/world.wbt

2. run SLAVE robot controller by:
    ```python
    python slave_controller.py
    ```
3. when you see in console "network init done" -> click play button in the Webots application

If you want to re-run slave_controller.py you need to:
  * restart Webots 
  * follow the Run Instruction from the 2nd point