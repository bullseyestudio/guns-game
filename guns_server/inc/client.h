/*

 Define what a client is and what it can do

*/
#ifndef GUNS_SERVER_CLIENT_H
#define GUNS_SERVER_CLIENT_H

class tClient
{
private:
	UDTSOCKET sock;

public:
	tClient(UDTSOCKET s): sock(s) {}

	string ReceiveMessage();
};

#endif // GUNS_SERVER_CLIENT_H
