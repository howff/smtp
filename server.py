#!/usr/bin/env python3

import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Message
from aiosmtpd.smtp import AuthResult, LoginPassword
from email.message import EmailMessage
import ssl
import time


# ========== AUTHENTICATOR ==========
class Authenticator:
    def __init__(self):
        pass
    def __call__(self, server, session, envelope, mechanism, auth_data):
        # Allow everyone!
        return AuthResult(success=True)


# ========== MESSAGE HANDLER ==========
class MailHandler():
    async def handle_DATA(self, server, session, envelope):
        # Display message on console
        print("=== Email Received ===")
        print("From:", envelope.mail_from)
        print("To:", envelope.rcpt_tos)
        print("Body:\n", envelope.content.decode('utf-8', errors='replace'))
        print("======================")
        # Respond to sender
        return "250 Message accepted"

# ========== CONTROLLER ==========
def main():
    # SSL context for STARTTLE
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("server.pem", "server.key")  # your cert + key

    #loop = asyncio.new_event_loop()

    controller = Controller(
        handler = MailHandler(),
        hostname="", # All interfaces
        port=8587,
        auth_required=True,
        authenticator=Authenticator(),
        tls_context=context,
        require_starttls=True,
        #loop=loop,
    )

    controller.start()
    print("SMTP server with STARTTLS running on port 8587...")
    controller._thread.join()

    #try:
    #    #asyncio.get_event_loop().run_forever()
    #    #loop.run_forever()
    #    time.sleep(1)
    #except KeyboardInterrupt:
    #    print("Shutting down...")
    #    controller.stop()
    #    #loop.stop()


if __name__ == "__main__":
    main()
