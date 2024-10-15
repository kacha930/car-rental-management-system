
from random import randint, choice as rc



from faker import Faker


from app import app
from models import db, Customer, CustomerProfile, Car, Rental

if __name__ == '__main__':
    fake = Faker()

    with app.app_context():
        print("Starting seed...")

        # Drop and create all tables
        db.drop_all()
        db.create_all()

        # Seed customer profiles
        customer_profiles = []
        for _ in range(10):
            profile = CustomerProfile(
                bio=fake.text(max_nb_chars=200),
                social_links=fake.url(),
                created_at=fake.date_time_this_year()
            )
            customer_profiles.append(profile)
            db.session.add(profile)

        db.session.commit()

        # Seed customers
        customers = []
        for profile in customer_profiles:
            customer = Customer(
                name=fake.name(),
                email=fake.email(),
                phone_number=fake.phone_number(),
                address=fake.address(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=75),
                profile_id=profile.id
            )
            customers.append(customer)
            db.session.add(customer)

        db.session.commit()

        # Seed cars
        cars = []
        for _ in range(20):
            car = Car(
                model=fake.word(),
                brand=rc(['Toyota', 'Honda', 'Ford', 'BMW', 'Audi']),
                year=randint(2000, 2023),
                price_per_day=round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
                availability_status=rc([True, False]),
                color=fake.color_name()
            )
            cars.append(car)
            db.session.add(car)

        db.session.commit()

        # Seed rentals
        for _ in range(30):
            rental = Rental(
                start_date=fake.date_time_this_year(),
                end_date=fake.date_time_this_year(),
                total_price=round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
                status=rc(['booked', 'completed', 'cancelled']),
                booking_date=fake.date_time_this_year(),
                customer_id=rc(customers).id,
                car_id=rc(cars).id
            )
            db.session.add(rental)

        db.session.commit()

        print("Seeding completed!")
