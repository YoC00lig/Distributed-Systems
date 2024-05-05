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
        auto calc = Ice::checkedCast<Ice::ObjectPrx>(base);

        try
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
                cout << result << endl;
            }
            else
            {
                cout << "UNKNOWN OPERATION" << endl;
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

