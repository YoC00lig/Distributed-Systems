#include <Ice/Ice.h>
#include "calculator.cpp"

using namespace std;
using namespace Demo;
using namespace Ice;

int main(int argc, char* argv[]) {
    int status = 0;
    CommunicatorPtr communicator;

    try {
        communicator = Ice::initialize(argc, argv);

        auto base = communicator->stringToProxy("calc/calc11:tcp -h 127.0.0.1 -p 10000");
        auto calc = Ice::checkedCast<CalcPrx>(base);

        try
        {
            {
                std::vector<Ice::Byte> inParams, outParams;

                Ice::OutputStream out(communicator);
                out.startEncapsulation();
                int x = 100, y = -1;
                out.write(x);
                out.write(y);
                out.endEncapsulation();
                out.finished(inParams);

                if(calc->ice_invoke("add", Ice::OperationMode::Idempotent, inParams, outParams))
                {
                    InputStream in(communicator, outParams);
                    in.startEncapsulation();
                    int result;
                    in.read(result);
                    in.endEncapsulation();
                    cout << "Wynik dodawania: " << result << endl;
                }
                else
                {
                    cout << "UNKNOWN OPERATION" << endl;
                }
            }

            {
                std::vector<Ice::Byte> inParams, outParams;

                Ice::OutputStream out(communicator);
                out.startEncapsulation();
                int x = 10, y = 5;
                out.write(x);
                out.write(y);
                out.endEncapsulation();
                out.finished(inParams);

                if(calc->ice_invoke("subtract", Ice::OperationMode::Idempotent, inParams, outParams))
                {
                    InputStream in(communicator, outParams);
                    in.startEncapsulation();
                    int result;
                    in.read(result);
                    in.endEncapsulation();
                    cout << "Wynik odejmowania: " << result << endl;
                }
                else
                {
                    cout << "UNKNOWN OPERATION" << endl;
                }
            }

            {
                std::vector<Ice::Byte> inParams, outParams;

                Ice::OutputStream out(communicator);
                out.startEncapsulation();
                A a;
                a.a = 5;
                a.b = 10;
                a.c = 3.14;
                a.d = "Hello";
                out.write(a);
                short b = 2;
                out.write(b);
                out.endEncapsulation();
                out.finished(inParams);

                if(calc->ice_invoke("op", Ice::OperationMode::Idempotent, inParams, outParams))
                {
                    cout << "Operacja na strukturze A wykonana pomyślnie." << endl;
                }
                else
                {
                    cout << "UNKNOWN OPERATION" << endl;
                }
            }
        }
        catch(const Ice::LocalException& ex)
        {
            cerr << ex << endl;
            status = 1;
        }

    } catch (const Ice::Exception& ex) {
        cerr << ex << endl;
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
