Everything is Trainable
=======================
Trainable is a open source web application for targeted Training control.

Trainable let you define custom trainings goals for which a trainingplan
can be created.
Trainable will stay in the background and anaylse your workout data to give
feedback about your progress on the way to the training goal.

Targeted Training
-----------------
The core of the goal-oriented training is to help the athlete achieve his or
her goals.

Therefor trainable provides some tools for the performanance diagnostics find
the athlets weakness to identify the worthy points where the athlete can
improve. Once the goals are defined trainable let you define your training
plan planning training units in detail. While tracking your workouts you can
link those workouts to the trainingunit and see how well you achieve the
objectives of training unit.

Performanance diagnostics
^^^^^^^^^^^^^^^^^^^^^^^^^
Currently not implemented

Currently Planned:

        - Critical Power Tests (CP)
        - Aerobic endurance (Steptests to find your heartrate/power at lactate threshold)

Trainingplan with goals
^^^^^^^^^^^^^^^^^^^^^^^
Currently not implemented

Currently Planned:

        - Google calender integration
        - Predefined and custum training units

Workout tracking
^^^^^^^^^^^^^^^^
Trainable uses Strava as its main source for training data. So athlets can
continue to use their favorite tracking software. However trainable provides
some additional fields to get a better option to use trainable as your logbook
for your workouts.

        - Distance
        - Duration
        - Time
        - RPE (Borg15)
        - Average Hearrate
        - Description
        - Athlets bio data like rest heartrate,weight or sleep
        - External circumstances like weather, wind etc.

Statistics/Evaluation
^^^^^^^^^^^^^^^^^^^^^
Currently not implemented



Getting Started
---------------

- cd <directory containing this file>

- $venv/bin/python setup.py develop

- $venv/bin/trainable-admin db init

- $venv/bin/pserve development.ini
