
# https://github.com/FiloSottile/mkcert/tree/v1.4.4
curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"
chmod +x mkcert-v*-linux-amd64
sudo mv mkcert-v*-linux-amd64 /usr/local/bin/mkcert


mkcert -install
mkcert localhost 127.0.0.1 ::1
mv localhost+2.pem cert.pem
mv localhost+2-key.pem key.pem