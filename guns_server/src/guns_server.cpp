/*

 Main entry point for the Guns server.

*/

#include <iostream>
using namespace std;

#include "constants.h"

int InitNetwork();

int main(int argc, char* argv[])
{
	cout << "Guns! dedicated server, v. " << VERSION << ". © 2011 narc0tiq." << endl;

	if(InitNetwork()) // any non-zero is an error
	{
		cerr << "Error in opening network, bailing..." << endl;
		return 1;
	}

	cout << "Doesn't do anything yet, sorry!" << endl;

	return 0;
}
