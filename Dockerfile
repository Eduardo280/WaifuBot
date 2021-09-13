# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev

FROM programmingerror/ultroid:b0.1

# set timezone
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# clone the repo and change workdir
RUN git clone https://github.com/fnixdev/WaifuBot.git /root/fnixdev/
WORKDIR /root/fnixdev/

# install main requirements.
COPY requirements.txt /deploy/
RUN pip3 install --no-cache-dir -r /deploy/requirements.txt

# install addons requirements
RUN wget -O /deploy/addons.txt https://git.io/JWdOk
RUN pip3 install --no-cache-dir -r /deploy/addons.txt

# start the bot
CMD ["bash", "resources/startup/startup.sh"]
