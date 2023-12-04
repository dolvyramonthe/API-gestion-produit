FROM python:3.9

WORKDIR /App

COPY . .

RUN apt-get update && apt-get install -y python3-apt

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

# EXPOSE 5000

COPY App.py /App
# CMD ["python", "App.py"]

CMD ["gunicorn", "App:app", "-b", "0.0.0.0:5000"]
