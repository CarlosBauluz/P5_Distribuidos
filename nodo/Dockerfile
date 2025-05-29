FROM python:3.11.4-slim
COPY node.py .
RUN pip install flask flask-socketio eventlet requests
CMD ["python", "node.py"]