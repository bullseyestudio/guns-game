/*

 Define how a client does what it does

*/

#include <iostream>
#include <udt.h>

using namespace std;

#include "client.h"

string tClient::ReceiveMessage()
{
	char data[100];

	if (UDT::ERROR == UDT::recvmsg(sock, data, 100))
	{
		cout << "recvmsg:" << UDT::getlasterror().getErrorMessage() << endl;
		return NULL;
	}

	return data;
}
