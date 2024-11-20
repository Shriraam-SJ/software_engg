import java.util.*;

public class Transaction {
    private Scanner sc = new Scanner(System.in);
    private String ACCOUNTNAME = "peter";
    private String ACCOUNTNUMBER = "12345";
    private String USERID = "peter@123";
    private String UPIID = "upi@123";
    private String CVVNUM = "123";
    private String PASSWORD = "12345";
    private int BALANCE = 100000;
    private String MPIN = "12345";


    public boolean DEBITCARD()
    {
        System.out.print("Enter account name: ");
        String name = sc.nextLine();
        if(name.equals(ACCOUNTNAME)){
            System.out.print("Enter account number: ");
            String number = sc.nextLine();
          if(number.equals(ACCOUNTNUMBER)){
            System.out.print("Enter CVV: ");
            String cvv = sc.nextLine();
           if(cvv.equals(CVVNUM)){
                System.out.println("ENTER THE AMOUNT ");
                int AMOUNT = sc.nextInt();
                BALANCE -= AMOUNT;
                return true;
           }
            else{
                System.out.println("INCORRECT CVV NUMBER!");
            }
        }
        else{
            System.out.println("INCORRECT ACCOUNT NUMBER!");
        }
      }
      else{
        System.out.println("ACCOUNT NAME NOT FOUND!");
      }return false;
    }


    public boolean CREDITCARD()
    {
        System.out.print("Enter account name: ");
        String name = sc.next();
        if(name.equals(ACCOUNTNAME)){
            System.out.print("Enter account number: ");
            String number = sc.next();
        if(number.equals(ACCOUNTNUMBER)){
            System.out.print("Enter CVV: ");
            String cvv = sc.next();
            if(cvv.equals(CVVNUM)){
                System.out.println("ENTER THE AMOUNT ");
                int AMOUNT = sc.nextInt();
                BALANCE -= AMOUNT;
                return true;
            }
            else{
                System.out.println("INCORRECT CVV NUMBER!");
            }
        }
        else{
            System.out.println("INCORRECT ACCOUNT NUMBER!");
        }
      }
      else{
        System.out.println("ACCOUNT NAME NOT FOUND!");
      }return false;


    }


    public boolean NETBANKING() {
            System.out.println("\nENTER THE USER ID: ");
            String userid = sc.next();
        if (userid.equals(USERID)){
                System.out.println("ENTER THE PASSWORD: ");
                String password = sc.next();
            if (password.equals(PASSWORD)){
                System.out.println("ENTER THE AMOUNT ");
                int AMOUNT = sc.nextInt();
                BALANCE -= AMOUNT;
                return true;
            } else {
                System.out.println("INVALID PASSWORD");
            }
        } else {
            System.out.println("INVALID USER ID");
        }
        return false;
    }


    public boolean UPI() {
        System.out.println("\nENTER THE UPI ID: ");
        String upiid = sc.next();
        if (upiid.equals(UPIID)){
            System.out.println("ENTER THE AMOUNT ");
            int AMOUNT = sc.nextInt();
            System.out.println("\nENTER THE MPIN: ");
            String mpin = sc.next();
            if (mpin.equals(MPIN)) {
                BALANCE -= AMOUNT;
                return true;
            } else {
                System.out.println("INVALID MPIN");
            }
        } else {
            System.out.println("INVALID UPI ID ");
        }
        return false;
    }


    public boolean pass()
    {
        System.out.println("ENTER OLD PASSWD : ");
        String pass = sc.next();
        if(pass.equals(PASSWORD))
        {
            System.out.println("ENTER NEW PASSWD : ");
            String newpass = sc.next();
            System.out.println("RE ENTER PASSWD : ");
            String npass = sc.next();
            if(newpass.equals(npass))
            {
                PASSWORD = newpass;
                return true;
            }
            else{
                System.out.println("WRONG PASSWD");
            }
        }
        else{
            System.out.println("INVALID PASSWD");
        }return false;
    }

    public int getBalance() {
        return BALANCE;
    }


    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Transaction transaction = new Transaction();
        boolean Request = false;
        while (!Request) {
        System.out.println("1. DEBIT CARD");
        System.out.println("2. CREDIT CARD");
        System.out.println("3. NET BANKING");
        System.out.println("4. UPI");
        System.out.println("5. CHECK BALANCE");
        System.out.println("6. CHANGE PASSWD");
        System.out.println("7. EXIT");
        System.out.print("ENTER YOUR MODE OF TRANSACTION : ");
       
        int choice = sc.nextInt();
       
        switch (choice) {
            case 1:{
                boolean success = transaction.DEBITCARD();
                if (success) {
                    System.out.println("AMOUNT TRANSFERED BY DEBIT CARD SUCCESSFULLY, AVAILABLE BALANCE: $" + transaction.getBalance());
                } else {
                    System.out.println("AMOUNT NOT TRANSFERED, AVAILABLE BALANCE: $" + transaction.getBalance());
                }
                break;
            }
            case 2:
            {
                boolean success = transaction.CREDITCARD();
                if (success) {
                    System.out.println("AMOUNT TRANSFERED BY CREDIT CARD SUCCESSFULLY, AVAILABLE BALANCE: $" + transaction.getBalance());
                } else {
                    System.out.println("AMOUNT NOT TRANSFERED, AVAILABLE BALANCE: $" + transaction.getBalance());
                }
                break;
            }
            case 3: {
                boolean success = transaction.NETBANKING();
                if (success) {
                    System.out.println("UPI TRANSACTION SUCCESSFULLY, AVAILABLE BALANCE: $" + transaction.getBalance());
                } else {
                    System.out.println("AMOUNT NOT TRANSFERED, AVAILABLE BALANCE: $" + transaction.getBalance());
                }
                break;
            }
           
            case 4: {
                boolean success = transaction.UPI();
                if (success) {
                    System.out.println("TRANSACTION SUCCESSFUL, AVAILABLE BALANCE: $" + transaction.getBalance());
                } else {
                    System.out.println("TRANSACTION NOT SUCCESSFUL, AVAILABLE BALANCE: $" + transaction.getBalance());
                }
                break;
            }
            
            case 5:
            {
                System.out.println("Current Balance: $" + transaction.getBalance());
                    break;
            }
            case 6:
            {
                boolean success = transaction.pass();
                if(success)
                {
                    System.out.println("PASSWD CHANGED SUCCESFULLY");
                }
                break;
            }
            case 7:
            {
                Request=true;
                break;
            }
            default:
                System.out.println("INVALID CHOICE");
                break;
        }
}
        System.out.println("\nThank you for using our banking system!");
        System.out.println("Account holder: " + transaction.USERID);
        System.out.println("Final balance: $" + transaction.getBalance());
        sc.close();
    }
}
