//  Hello World server

#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>

//char* serv = "tcp://0.0.0.0:2222";
//char* serv = "tcp://vlan2:3333";
//char* serv = "tcp://localhost:3333";
char* serv = "tcp://*:3333";

int main (void)
{
    //  Socket to talk to clients
    void *context = zmq_ctx_new ();
    //void *context = zmq_init(1);
    void *responder = zmq_socket (context, ZMQ_REP);
    int rc = zmq_setsockopt (responder, ZMQ_SUBSCRIBE, "", 0);
    //void *responder = zmq_socket (context, ZMQ_NOBLOCK);
    rc = zmq_bind (responder, serv);
    printf("Err: %s\n", zmq_strerror(errno));
    assert (rc == 0);

    while (1) {
      char buffer [10];
      //char tmp[256];
      //memset(tmp, 0, 256);
      
      //zmq_msg_t msg;
      //int rc = zmq_msg_init_size (&msg, 10);
      
      rc = zmq_recv (responder, buffer, 10, 0);
      int more = 0;
      size_t size = sizeof(int); // 1
      zmq_getsockopt(responder, ZMQ_RCVMORE, &more, &size); // 2
      if (rc > 0) {
          buffer[rc]='\x00';
          //zmq_recv (responder, &msg, 0);
          printf ("Received: %s, Length: %ld", buffer, rc);
          sleep (1);          //  Do some 'work'
          if(more) {
              printf(" - reading also...\n");
          } else {
              printf(" - done\n");
          }

          //zmq_send (responder, "Worl", 4, ZMQ_SNDMORE);

          //sprintf("");
          zmq_send (responder, "World", 5, 0);
          //memset (zmq_msg_data (&msg), "World", 6);
          //zmq_send (responder, &msg, 0);
      } else {
          printf ("Error: null is receiver!\n", buffer);
      }
    }
    zmq_close(responder); // destructors
    //rc = zmq_term(context);
    return 0;
}
