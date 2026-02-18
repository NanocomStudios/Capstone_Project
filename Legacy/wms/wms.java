import java.net.*;
import java.io.*;
import java.util.*;

class Inventory{
    enum ItemState{
        ARRIVED,
        PACKED,
        SHIPPED
    }

    private static Map<Integer, ItemState> inventory = new TreeMap<>();
    private static Integer lastID = 0;

    public static synchronized Integer addItem(){
        Integer tmpID = lastID;
        inventory.put(tmpID, ItemState.ARRIVED);
        Server.publish("added " + tmpID);
        lastID++;
        return tmpID;
    }

    public static synchronized Boolean packItem(Integer id){
        if(inventory.containsKey(id) && inventory.get(id) == ItemState.ARRIVED) {
            inventory.put(id, ItemState.PACKED);
            Server.publish("packed " + id);
            return true;
        }else{
            return false;
        }
    }

    public static synchronized Boolean shipItem(Integer id){
        if(inventory.containsKey(id) && inventory.get(id) == ItemState.PACKED) {
            inventory.put(id, ItemState.SHIPPED);
            Server.publish("shipped " + id);
            return true;
        }else{
            return false;
        }
    }
    

    public static synchronized ItemState getItemState(Integer id){
        if(inventory.containsKey(id)) {
            return inventory.get(id);
        }
        return null;
    }

    public static synchronized Map<Integer, ItemState> getItemList(){
        return inventory;
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
        System.out.println("published: " + msg);
        for(Client client : clients){
            try{
                client.out.write((msg + '\r' + '\n').getBytes());
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
            out.write(("Warehouse Management Portal\r\n").getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void run() {

        WarehouseHandler warehouse = new WarehouseHandler();

        try {
            String m = "";
            while (true) {
                char c = (char) in.read();
                if(c == '\n') {
                    m = m.trim();

                    String res = warehouse.execute(m);

                    if(res == "listen"){
                        Server.newListner(s,in,out);
                        out.write(("listning\r\n").getBytes());
                    }else{
                        out.write((res + "\r\n").getBytes());
                    }

                    if(res == "terminated"){
                        return;
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

class WarehouseHandler{

    public String execute(String input){
        String[] inputList = input.split(" ");
        Integer id;

        switch (inputList[0]) {
            case "exit":
                return("terminated");
            case "listen":
                return("listen");
            case "add":
                id = Inventory.addItem();
                return("added " + id);
            case "pack":
                if(inputList.length > 1) {
                    try {
                        id = Integer.parseInt(inputList[1]);
                        if(Inventory.packItem(id)){
                            return("packed " + id);
                        }else{
                            return("error item_not_found");
                        }
                    } catch (NumberFormatException e) {
                        return("error invalid_ID");
                    }
                } else {
                    return("error missing_ID");
                }
            case "ship":
                if(inputList.length > 1) {
                    try {
                        id = Integer.parseInt(inputList[1]);
                        if(Inventory.shipItem(id)){
                            return("shipped " + id);
                        }else{
                            return("error item_not_found");
                        }
                    } catch (NumberFormatException e) {
                        return("error invalid_ID");
                    }
                } else {
                    return("error missing_ID");
                }
            case "state":
                if(inputList.length > 1) {
                    try {
                        id = Integer.parseInt(inputList[1]);
                        Inventory.ItemState state = Inventory.getItemState(id);
                        if(state != null) {
                            return(id + " " + state);
                        } else {
                            return("error item_not_found");
                        }
                    } catch (NumberFormatException e) {
                        return("error invalid_ID");
                    }
                } else {
                    return("error missing_ID");
                }
            case "list":
                Map<Integer, Inventory.ItemState> itemList = Inventory.getItemList();
                String output = "";

                for (Integer key : itemList.keySet()) {
                    output += key + " " + itemList.get(key) + "\r\n";
                }
                output += "done";
                return output;
            case "":
                return("");

            default:
                return("error unknown_command");
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

        WarehouseHandler warehouse = new WarehouseHandler();

        String input = "";
        do{
            input = System.console().readLine();

            String res = warehouse.execute(input);

            if(res == "listen"){
                System.out.println("Cannot join as a listner!");
            }else{
                System.out.println(res);
            }

            if(res == "terminated"){
                System.exit(0);
            }

        }while(true);

    }
}