# import random
# import asyncio
# import aiosmtplib
# from email.message import EmailMessage

# async def send_otp_email():
#     otp=""
#     for i in range(5):
#         otp += str(random.randint(0, 9))

#       # Input email
#     to_mail = input("Enter your email address: ")

#     # Email content
#     msg = EmailMessage()
#     msg['Subject'] = "OTP Verification"
#     msg['From'] = "kamaljungkarki13579@gmail.com"
#     msg['To'] = to_mail
#     msg.set_content(f"Your OTP is: {otp}")

#     # Send email using aiosmtplib
#     server = aiosmtplib.SMTP(hostname='smtp.gmail.com', port=465, use_tls=True)
#     await server.connect()
#     await server.login("kamaljungkarki13579@gmail.com", "lpgcdftcldjvrnlx")
#     await server.send_message(msg)
#     await server.quit()

#     print("OTP sent successfully to " + to_mail)

#     # Verify OTP
#     input_otp = input("Enter the OTP sent to your email: ")
#     if input_otp == otp:
#         print("OTP verified successfully!")
#     else:
#         print("Invalid OTP. Please try again.")


# # Run the async function
# asyncio.run(send_otp_email())
