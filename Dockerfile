FROM zironycho/jpype3

WORKDIR /app

# build-base is for building from sources (gevent)
RUN pip install --upgrade pip
RUN apk add --no-cache build-base

# copy module sources
COPY src ./src

# copy setup files
COPY setup.py setup.cfg README.md MANIFEST.in LICENSE ./

# install module
RUN python setup.py install

# install gunicorn server
RUN pip install gunicorn
RUN pip install --no-binary gevent gevent

# set gunicorn run mode
# $PORT is set by Heroku or the --env-vars argument, set default to 80
ENV G_PORT=${PORT:-80}
ENV NUM_WORKERS=2

# open default http port
EXPOSE $G_PORT

# Run the app. CMD is required to run on Heroku (vs ENTRYPOINT)
CMD gunicorn -w $NUM_WORKERS --bind=0.0.0.0:$G_PORT -k gevent 'llapp.__main__:create_app()'
