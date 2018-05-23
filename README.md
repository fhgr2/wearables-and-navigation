# wearables-and-navigation

## src

### Start Flask

Call

    start-flask-dev.sh

which then starts

    flask-app.py

which will start/stop

    main.py

### Start `main.py` directly:

    cd src/; export GPIOZERO_PIN_FACTORY=mock; ./main.py --lat 46.85449 --lon 9.52864

Explanation:

- Setting `GPIOZERO_PIN_FACTORY` is necessary (only) on systems that are not a Raspberry Pi
- `--lat` and `--lon` are the destination coordinates (these are necessary)


## test1

Read way from Chur Bahnhof to Medienhaus, display waypoints, instruction and angle in console.
Next step: Make simulation on a map for position, compare then simulated position with angle.

## test2

- Generate fake gps data and read it from python
- Calculate distance to linestring

## Links

- https://docs.google.com/document/d/***REMOVED***/edit
