
import json
import os


class FoodDonationSystem:

    def __init__(self):
        self.users_file = "users.json"
        self.donations_file = "donations.json"

        self.users = self.load_data(self.users_file)
        self.donations = self.load_data(self.donations_file)

    # Load JSON data
    def load_data(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, OSError):
                print("Warning: Could not read", filename)

        return []

    # Save JSON data
    def save_data(self):
        with open(self.users_file, "w") as file:
            json.dump(self.users, file, indent=4)

        with open(self.donations_file, "w") as file:
            json.dump(self.donations, file, indent=4)

    # Register user
    def register_user(self):
        name = input("Enter name: ").strip()
        role = input("Enter role (Donor/Volunteer): ").strip().title()
        contact = input("Enter contact: ").strip()

        if not name or not contact:
            print("Name and contact are required!")
            return

        if role not in ["Donor", "Volunteer"]:
            print("Invalid role!")
            return

        user_id = f"USR{len(self.users) + 1:03d}"

        user = {
            "user_id": user_id,
            "name": name,
            "role": role,
            "contact": contact
        }

        self.users.append(user)
        self.save_data()

        print("User registered successfully!")
        print("User ID:", user_id)

    # Create food donation
    def create_donation(self):
        donor_id = input("Enter Donor ID: ").strip()

        donor = next(
            (u for u in self.users
             if u["user_id"] == donor_id
             and u["role"] == "Donor"),
            None
        )

        if donor is None:
            print("Invalid donor ID!")
            return

        food = input("Enter food name: ").strip()

        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                raise ValueError
        except ValueError:
            print("Quantity must be a positive number!")
            return

        location = input("Enter location: ").strip()
        expiry = input("Available until: ").strip()

        if not all([food, location, expiry]):
            print("All donation details are required!")
            return

        donation_id = f"DON{len(self.donations) + 1:03d}"

        donation = {
            "donation_id": donation_id,
            "food": food,
            "quantity": quantity,
            "location": location,
            "expiry": expiry,
            "contact": donor["contact"],
            "donor_id": donor_id,
            "volunteer_id": None,
            "status": "Available"
        }

        self.donations.append(donation)
        self.save_data()

        print("\nDonation created successfully!")
        print("Donation ID:", donation_id)
        print("Status: Available")

    # View available donations
    def view_donations(self):
        print("\n--- AVAILABLE DONATIONS ---")

        found = False

        for donation in self.donations:
            if donation["status"] == "Available":
                found = True

                print("\nDonation ID:", donation["donation_id"])
                print("Food:", donation["food"])
                print("Quantity:", donation["quantity"])
                print("Location:", donation["location"])
                print("Available Until:", donation["expiry"])
                print("Status:", donation["status"])

        if not found:
            print("No available donations.")

    # Claim donation
    def claim_donation(self):
        volunteer_id = input("Enter Volunteer ID: ").strip()

        volunteer = next(
            (u for u in self.users
             if u["user_id"] == volunteer_id
             and u["role"] == "Volunteer"),
            None
        )

        if volunteer is None:
            print("Invalid volunteer ID!")
            return

        donation_id = input("Enter Donation ID: ").strip()

        for donation in self.donations:

            if donation["donation_id"] == donation_id:

                if donation["status"] != "Available":
                    print("Donation is not available!")
                    return

                donation["status"] = "Claimed"
                donation["volunteer_id"] = volunteer_id

                self.save_data()

                print("Donation claimed successfully!")
                return

        print("Donation not found!")

    # Update donation status
    def update_status(self):
        donation_id = input("Enter Donation ID: ").strip()

        donation = next(
            (d for d in self.donations
             if d["donation_id"] == donation_id),
            None
        )

        if donation is None:
            print("Donation not found!")
            return

        volunteer_id = input("Enter Volunteer ID: ").strip()

        if donation["volunteer_id"] != volunteer_id:
            print("This donation is not assigned to you!")
            return

        next_status = {
            "Claimed": "Picked Up",
            "Picked Up": "Delivered"
        }

        current = donation["status"]

        if current not in next_status:
            print("Invalid status update!")
            return

        donation["status"] = next_status[current]

        self.save_data()

        print("Status updated successfully!")
        print("New Status:", donation["status"])

    # Display all donations
    def view_all(self):
        print("\n--- ALL DONATION RECORDS ---")

        if not self.donations:
            print("No donation records found.")
            return

        for donation in self.donations:
            print(donation)

    # Main menu
    def menu(self):

        while True:

            print("\n================================")
            print(" FOOD DONATION MANAGEMENT SYSTEM")
            print("================================")
            print("1. Register User")
            print("2. Create Donation")
            print("3. View Available Donations")
            print("4. Claim Donation")
            print("5. Update Donation Status")
            print("6. View All Donations")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.register_user()

            elif choice == "2":
                self.create_donation()

            elif choice == "3":
                self.view_donations()

            elif choice == "4":
                self.claim_donation()

            elif choice == "5":
                self.update_status()

            elif choice == "6":
                self.view_all()

            elif choice == "7":
                self.save_data()
                print("Thank you for using the system!")
                break

            else:
                print("Invalid choice! Try again.")


# Run application
if __name__ == "__main__":
    app = FoodDonationSystem()
    app.menu()
