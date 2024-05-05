#include <Ice/Ice.h>
#include "calculator.h"

using namespace Demo;
using namespace std;

int main(int argc, char* argv[]) {
    int status = 0;
    Ice::CommunicatorPtr communicator;

    try {
        // Inicjalizacja Ice communicatora
        communicator = Ice::initialize(argc, argv);

        // Uzyskanie referencji do obiektu zdalnego na podstawie linii konfiguracyjnej
        Ice::ObjectPrx base = communicator->stringToProxy("calc11:tcp -h 127.0.0.1 -p 10000 -z");

        // Rzutowanie referencji do interfejsu Calc
        CalcPrx calc = CalcPrx::uncheckedCast(base);
        if (!calc) {
            throw "Invalid proxy";
        }

        // Wywołanie zdalnych operacji
        long resultAdd = calc->add(7, 8);
        long resultSubtract = calc->subtract(10, 5);

        cout << "Result of addition: " << resultAdd << endl;
        cout << "Result of subtraction: " << resultSubtract << endl;

    } catch (const Ice::Exception& ex) {
        cerr << ex << endl;
        status = 1;
    } catch (const char* msg) {
        cerr << "Error: " << msg << endl;
        status = 1;
    }

    if (communicator) {
        try {
            communicator->destroy();
        } catch (const Ice::Exception& ex) {
            cerr << ex << endl;
            status = 1;
        }
    }

    return status;
}
