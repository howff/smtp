# SMTP server

Supports STARTTLS.

Does not check any credentials so you can authenticate as anybody.

Uses a self-signed certificate.

Uses aiosmtpd (asyncio smtpd) not the old built-in library smtpd that is deprecated.

Runs on port 8587 (to mirror the standard port 587).

# Create certificate

This will create a self-signed certificate:
```
openssl req -x509 -nodes -newkey rsa:2048   -keyout server.key -out server.pem -days 365   -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"
```

If you have created a domain certificate then use it instead; you can use the concatenated chain version.

# Test without container

```
python3 -m venv venv
source venv/bin/activate
pip install aiosmtpd
./server.py
```

# Build container

```
sudo docker build -t smtpserver .
sudo docker tag smtpserver ghcr.io/howff/smtpserver
sudo docker push ghcr.io/howff/smtpserver
```

# Run container

Look in the docker logs to see the emails which have been sent.
```
sudo docker run -d --name smtpserver -p 8587:8587 smtpserver
sudo docker logs -f smtpserver
```

If you want to replace the certificate:
```
sudo docker run -d --name smtpserver -p 8587:8587 -v server.chain_pem:/server.pem smtpserver
```

# Test certificate

```
openssl s_client -starttls smtp -connect localhost:8587 -showcerts
```

# Test with a client

```
./client.py
```
