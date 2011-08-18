/*

 Defines some global constants of interest

*/
#ifndef GUNS_SERVER_CONSTANTS_H
#define GUNS_SERVER_CONSTANTS_H

static const string VERSION = "0.01"; // server version
static const int LISTEN_PORT = 44000; // listen port

// This is the time the "select" waits before timing out. 50ms = 20 FPS max.
static const long COMMS_WAIT_SEC = 0;        // time to wait in seconds
static const long COMMS_WAIT_USEC = 50000;  // time to wait in microseconds

#endif // GUNS_SERVER_CONSTANTS_H
