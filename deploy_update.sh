# This assumes git was set up.
git pull

# This assumes that nginx was set up.
sudo service nginx restart

# Nohup will keep the uvicron server up and running when the terminal closes.
nohup python3 -m uvicorn API:app --reload &