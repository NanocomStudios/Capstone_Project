import java.net.*;
import java.io.*;
import java.util.Vector;
import java.util.Map;

class Inventory{
    enum ItemState{
        ARRIVED,
        PACKED,
        SHIPPED
    }

    private static java.util.Map<Integer, ItemState> inventory = new java.util.HashMap<>();
    private static Integer lastID = 0;

    public static synchronized Integer addItem(){
        Integer tmpID = lastID;
        inventory.put(tmpID, ItemState.ARRIVED);
        lastID++;
        return tmpID;
    }

    public static synchronized void packItem(Integer id){
        if(inventory.containsKey(id) && inventory.get(id) == ItemState.ARRIVED) {
            inventory.put(id, ItemState.PACKED);
        }
    }

    public static synchronized void shipItem(Integer id){
        if(inventory.containsKey(id) && inventory.get(id) == ItemState.PACKED) {
            inventory.put(id, ItemState.SHIPPED);
        }
    }

    public static synchronized ItemState getItemState(Integer id){
        if(inventory.containsKey(id)) {
            return inventory.get(id);
        }
        return null;
    }
}

class Client{
    public Socket s;
    public DataInputStream in;
    public DataOutputStream out;

    public Client(Socket s_in, DataInputStream in_in, DataOutputStream out_in){
        s = s_in;
        in = in_in;
        out = out_in;
    }
}

class Server {
  
    // Initialize socket and input stream
    private ServerSocket ss = null;
    private static Vector<Client> clients = new Vector<>();

    public static void publish(String msg){
        for(Client client : clients){
            try{
                client.out.write((msg + '\n').getBytes());
            }catch (IOException e) {
            e.printStackTrace();
        }
        }
    }

    public static void newListner(Socket s, DataInputStream in, DataOutputStream out){
        clients.add(new Client(s,in,out));
    }

    public static void removeListners(){
        for(Client client : clients){
            try{
                client.s.close();
                client.in.close();
                client.out.close();
            }catch (IOException e) {
            e.printStackTrace();
        }
        }
    }

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
                        case "exit":
                            System.out.println("Closing connection");
                            return;
                        case "listen":
                            Server.newListner(s,in,out);
                            break;
                        default:
                            System.out.println(m);
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
            Integer id;

            switch (inputList[0]) {
                case "exit":
                    System.out.println("Terminating server");
                    System.exit(0);
                    break;
                case "add":
                    id = Inventory.addItem();
                    System.out.println("Item added with ID: " + id);
                    Server.publish("added " + id);
                    break;
                case "pack":
                    if(inputList.length > 1) {
                        try {
                            id = Integer.parseInt(inputList[1]);
                            Inventory.packItem(id);
                            System.out.println("Item packed with ID: " + id);
                            Server.publish("packed " + id);
                        } catch (NumberFormatException e) {
                            System.out.println("Invalid item ID");
                        }
                    } else {
                        System.out.println("Missing item ID");
                    }
                    break;
                case "ship":
                    if(inputList.length > 1) {
                        try {
                            id = Integer.parseInt(inputList[1]);
                            Inventory.shipItem(id);
                            System.out.println("Item shipped with ID: " + id);
                            Server.publish("shipped " + id);
                        } catch (NumberFormatException e) {
                            System.out.println("Invalid item ID");
                        }
                    } else {
                        System.out.println("Missing item ID");
                    }
                    break;
                case "state":
                    if(inputList.length > 1) {
                        try {
                            id = Integer.parseInt(inputList[1]);
                            Inventory.ItemState state = Inventory.getItemState(id);
                            if(state != null) {
                                System.out.println("Item state for ID " + id + ": " + state);
                            } else {
                                System.out.println("Item not found with ID: " + id);
                            }
                        } catch (NumberFormatException e) {
                            System.out.println("Invalid item ID");
                        }
                    } else {
                        System.out.println("Missing item ID");
                    }
                    break;
                default:
                    System.out.println("Unknown command");
                    break;
            }

        }while(!input.equals("terminate"));

    }
}