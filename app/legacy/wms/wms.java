import java.net.*;
import java.io.*;

class Server {
  
    // Initialize socket and input stream
    private ServerSocket ss = null;

    // Constructor with port
    public Server(int port) {
      
        // Starts server and waits for a connection
        try
        {
            ss = new ServerSocket(port);

        }catch (IOException e) {
            e.printStackTrace();
        }      
    }

    public ServerSocket getServerSocket() {
        return ss;
    }
}

class ServerThread extends Thread {
    private ServerSocket ss;

    public ServerThread(ServerSocket ss) {
        this.ss = ss;
    }

    public void run() {
        try {
            while (true) {
                System.out.println("Waiting for a client ...");

                Socket s = ss.accept();
                System.out.println("Client accepted");

                ClientHandler ch = new ClientHandler(s);
                ch.start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class ClientHandler extends Thread {
    private Socket s;
    private DataInputStream in;
    private DataOutputStream out;

    // Constructor
    public ClientHandler(Socket s) {
        this.s = s;
        try {
            this.in = new DataInputStream(new BufferedInputStream(s.getInputStream()));
            this.out = new DataOutputStream(s.getOutputStream());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void run() {
        try {
            String m = "";
            while (true) {
                char c = (char) in.read();
            
                if(c == '\n') {
                    m = m.trim();

                    String[] parts = m.split(" ");
                    
                    switch (parts[0]) {
                        case "terminate":
                            System.out.println("Closing connection");
                            return;
                        default:
                            break;
                    }
                    m="";
                }else {
                    m += c;
                }

            }
        } catch (IOException e) {
            e.printStackTrace();
            return;
        } finally {
            try {
                s.close();
                in.close();
                out.close();
            } catch (IOException e) {
                e.printStackTrace();
                return;
            }
        }
    }
}

public class wms {
    public static void main(String args[]){
        if(args.length < 1) {
            System.out.println("Error: port undefined");
            System.out.println("Usage: java wms <port>");
            return;
        }
        Server s = new Server(Integer.parseInt(args[0]));

        ServerThread st = new ServerThread(s.getServerSocket());
        st.start();

        String input = "";
        do{
            input = System.console().readLine();

            String[] inputList = input.split(" ");
            
            switch (inputList[0]) {
                case "terminate":
                    System.out.println("Terminating server");
                    System.exit(0);
                default:
                    System.out.println("Unknown command");
                    break;
            }

        }while(!input.equals("terminate"));

    }
}