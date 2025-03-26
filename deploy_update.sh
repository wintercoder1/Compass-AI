# This assumes git was set up.
git pull

# This assumes that nginx was set up.
sudo service nginx restart

# Nohup will keep the uvicron server up and running when the terminal closes.
# The server will use python3.11
nohup python3.12 -m uvicorn API:app --reload &