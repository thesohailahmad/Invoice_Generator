import json
class Service:
    def __init__(self,description,quantity,unit_price):
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
    @property
    def total(self):
        return self.quantity * self.unit_price

class Client:
    def __init__(self,name,phone,email,address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
    def show_info(self):
        return f"Name : {self.name}\nPhone : {self.phone}\nEmail : {self.email}\nAddress : {self.address}" 
    
class Invoice:
    def __init__(self, invoice_id, client):  
        self.invoice_id = invoice_id
        self.client = client
        self.services = []
        self.status = "Unpaid"
    def add_service(self,service):
        self.services.append(service)
    def subtotal(self):
        total = 0
        for service in self.services:
            total += service.total
        return total
    def grand_total(self):
        return self.subtotal()
    def to_dict(self):
        return {
            "invoice_id": self.invoice_id,
            "status": self.status,
            "client": {
                "name": self.client.name,
                "phone": self.client.phone,
                "email": self.client.email,
                "address": self.client.address
            },
            "services": [
                {
                    "description": s.description,
                    "quantity": s.quantity,
                    "unit_price": s.unit_price
                }
                for s in self.services
            ]
        }
class InvoiceManger:
    def __init__(self):
        self.invoices = []

    def add_invoice(self, invoice):
        self.invoices.append(invoice)

    def list_all(self):
        if not self.invoices:
            print("No invoices found.")
            return
        for invoice in self.invoices:
            print(f"  {invoice.invoice_id} | {invoice.client.name} | {invoice.status}")
    def get_invoice(self, invoice_id):
        for invoice in self.invoices:
            if invoice.invoice_id == invoice_id:
                return invoice
        return None

    def save_to_json(self):
        data = [invoice.to_dict() for invoice in self.invoices]
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Invoices saved to data.json!")



def display_invoice(invoice):
    print("=" * 45)
    print(f"  INVOICE #{invoice.invoice_id}")
    print("=" * 45)
    print(f"  Client  : {invoice.client.name}")
    print(f"  Phone   : {invoice.client.phone}")
    print(f"  Email   : {invoice.client.email}")
    print(f"  Address : {invoice.client.address}")
    print("-" * 45)
    print(f"  {'Service':<18} {'Qty':<5} {'Price':<8} {'Total'}")
    print("-" * 45)
    for service in invoice.services:
        print(f"  {service.description:<18} {service.quantity:<5} {service.unit_price:<8} {service.total:,}")
    print("-" * 45)
    print(f"  Subtotal    : {invoice.subtotal():>10,} PKR")
    print(f"  Grand Total : {invoice.grand_total():>10,} PKR")
    print(f"  Status      : {invoice.status}")
    print("=" * 45)
manager = InvoiceManger()
def create_invoice():
    print("\n--- Client Information ---")
    name    = input("Please Enter Client Name    : ").capitalize()
    phone   = input("Please Enter Phone          : ")
    email   = input("Please Enter Email          : ")
    address = input("Please Enter Address        : ").capitalize()

    client = Client(name, phone, email, address)

    invoice_id = input("\nPlease Enter Invoice ID (e.g. INV-001) : ").capitalize()
    invoice = Invoice(invoice_id, client)

    print("\n--- Add Services ---")
    while True:
        description = input("Please Enter Service Name   : ").capitalize()
        quantity    = int(input("Please Enter Quantity       : "))
        unit_price  = int(input("Please Enter Unit Price     : "))

        service = Service(description, quantity, unit_price)
        invoice.add_service(service)

        another = input("\n Do you want to Add another service? (y/n): ")
        if another.lower() != "y":
            break
    manager.add_invoice(invoice)
    print("\n--- Invoice Generated! ---\n")
    display_invoice(invoice)

def main():
    while True:
        print("INVOICE GENERATOR")
        print("1. Create New Invoice")
        print("2. View All Invoices")
        print("3. View Invoice by ID ")
        print("4. Save invoice")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_invoice()
        elif choice == "2":
            manager.list_all()
        elif choice == "3":
            invoice_id = input("Enter Invoice ID : ")
            invoice = manager.get_invoice(invoice_id)
            if invoice:
                display_invoice(invoice)
            else:
                print("Invoice not found!")
        elif choice == "4":
                manager.save_to_json()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

main()