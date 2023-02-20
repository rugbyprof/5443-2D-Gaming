import comms
import pika


def getConnections():
    # set RabbitMQ connection parameters
    credentials = pika.PlainCredentials('helper', 'rockpaperscissorslizardspock')
    parameters = pika.ConnectionParameters('terrywgriffin.com', 5672, '/', credentials)

    # create a connection to RabbitMQ
    connection = pika.BlockingConnection(parameters)

    # create a channel
    channel = connection.channel()

    print(dir(channel))
    print("="*50)
    print(dir(channel.connection))

    # # retrieve the list of current connections
    # connections = channel.connection_state()['connections']

    # # print the list of connections
    # print(f"Total number of connections: {len(connections)}")
    # for connection in connections:
    #     print(f"Connection {connection['name']} with protocol {connection['protocol']} from {connection['peer_address']}")

    # close the connection
    connection.close()



class MultiGamer:
    def __init__(self,**kwargs):
        self.gameId = kwargs.get('gameId',None)
        getConnections()
    


if __name__=='__main__':
    m = MultiGamer()
# rockpaperscissorslizardspock