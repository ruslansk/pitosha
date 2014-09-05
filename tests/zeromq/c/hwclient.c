//  Hello World client
#include <zmq.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>

//char* conn = "udp://localhost:2222";
//char* conn = "tcp://localhost:3333";
//char* conn = "tcp://192.168.1.1:2222";
#include "out/tests.h"

int main (void)
{
    printf ("Connecting to hello world server...\n");
    void *context = zmq_ctx_new ();
    //void *context = zmq_init (2);
    void *requester = zmq_socket (context, ZMQ_REQ);
    zmq_connect (requester, conn);

    int request_nbr;
    for (request_nbr = 0; request_nbr != 10; request_nbr++) {
        char buffer [100];
        //zmq_msg_t msg;
        //int rc = zmq_msg_init_size (&msg, 6);
        
        printf ("Sending Hello %d...\n", request_nbr);
        sprintf(buffer, "hai: %d\x00", request_nbr);
        zmq_send (requester, buffer, strlen(buffer), ZMQ_SNDMORE);
        sprintf(buffer, "haha: %d\x00", request_nbr);
        zmq_send (requester, buffer, strlen(buffer), 0);
        //memset (zmq_msg_data (&msg), "Hello", 6);
        //zmq_send (requester, &msg, 0);
        zmq_recv (requester, buffer, 10, 0);
        //zmq_recv (requester, &msg, 0);
        printf ("Received World %d\n", request_nbr);
    }
    zmq_close (requester);
    //zmq_term(context);
    zmq_ctx_destroy (context);
    return 0;
}
