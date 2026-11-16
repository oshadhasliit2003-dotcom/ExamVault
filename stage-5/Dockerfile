FROM python:3.12-slim
WORKDIR /srv/app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
RUN useradd -m portal && chown -R portal /srv/app
USER portal
ENV FLAG="EXAM{placeholder_set_FLAG_env}"
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "app:app"]
