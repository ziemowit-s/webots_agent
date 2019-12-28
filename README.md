Webots agent for Renforcement Learning

# Prerequisites
* Install spikeagents library from the spiking_neural_agents GitHub repo:
    ```bash
    pip install git+https://github.com/ziemowit-s/spiking_neural_agents.git
    ```

* Download stable Webots release: https://github.com/cyberbotics/webots/releases
* Install
* Add to .bashrc:
    ```bash
    export WEBOTS_HOME="/usr/local/webots"
    export LD_LIBRARY_PATH="$WEBOTS_HOME/lib/controller"
    export PYTHONPATH="$WEBOTS_HOME/lib/controller/python36:$PYTHONPATH"
    ```

# How to...
* If you want to deploy code from PyCharm
  * run ide from console write `pycharm-profesional` or `pycharm-community `in the console
  * this will use all environmental variable from your .bashrc
  
* Type `webots` from the console

* To start project in Webots: 
  * click Wizard
  * New Project Directory [Next] 
  * choose location [Next] 
  * name of your world file (with *.wbt extention) 
  * click "Add a rectangle area" [Next]
  * Finish 
  
* To add new object (box, robots):
  * click + sign
  * click PROTO nodes (Webots Projects)
  * to add robot click "robots" and choose one for you
  * gctronic->epuck-EPuck (Robot) is a robot with camera view
  
* To deploy code from PyCharm:
  * in Webots window select your robot on the node list
    * double click on the robot list element
    * click "controller"
    * click Select
    * choose "<Extern>"
  * In PyCharm
    * select run.py file and click run button
    * open Webots window and click run
  * This procedure run the code to the first robot which has "<extern>" param
  * If you have more robots - go to Webots docs and find how to run them

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