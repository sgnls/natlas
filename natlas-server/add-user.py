#!/usr/bin/env python3
import argparse
from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()

PASS_LENGTH = 16


def main():
	parser_desc = "Server-side utility to facilitate creating users. This is only meant to be used for bootstrapping, \
		as it prints the password to the command line."
	parser_epil = "Be sure that you're running this from within the virtual environment for the server, \
		otherwise it will almost certainly fail."
	parser = argparse.ArgumentParser(description=parser_desc, epilog=parser_epil)
	parser.add_argument("email", metavar="example@example.com", help="Email address of user to create or modify")
	parser.add_argument("--admin", action="store_true", default=False, help="Use this flag to make the user admin")
	args = parser.parse_args()

	validemail = User.validate_email(args.email)

	if not validemail:
		print(f"{args.email} does not appear to be a valid, deliverable email")
		return

	user = User.query.filter_by(email=validemail).first()
	if user is not None:
		if args.admin:
			if user.is_admin:
				print(f"User {validemail} is already an admin")
				return
			else:
				user.is_admin = True
				db.session.add(user)
				db.session.commit()
				print(f"User {validemail} is now an admin" % validemail)
				return
		else:
			print(f"User {validemail} already exists")
			return
	else:
		password = User.generate_password(PASS_LENGTH)
		user = User(email=validemail, is_admin=args.admin)
		user.set_password(password)
		db.session.add(user)
		db.session.commit()
		if user.is_admin:
			admintext = " as an admin "
		else:
			admintext = " "
		print(f"User {validemail} has been created{admintext}with password {password}")
		return


if __name__ == "__main__":
	main()
