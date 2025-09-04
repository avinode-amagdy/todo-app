# Todo App

A simple and elegant todo application built with Python Flask and SQLite, designed for deployment on Kubernetes using Helm and ArgoCD.

## Features

- ✅ Clean and modern web interface
- ✅ SQLite database for data persistence
- ✅ Add, complete, and delete todos
- ✅ Real-time task statistics
- ✅ RESTful API endpoints
- ✅ Health check endpoints for Kubernetes
- ✅ Containerized with Docker
- ✅ Kubernetes-ready with Helm charts
- ✅ GitOps deployment with ArgoCD

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the app:**
   Open your browser and go to `http://localhost:5000`

### Docker

1. **Build the image:**
   ```bash
   docker build -t todo-app:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 -v $(pwd)/data:/app/data todo-app:latest
   ```

## Kubernetes Deployment

### Using Helm

1. **Install the Helm chart:**
   ```bash
   helm install todo-app ./helm/todo-app
   ```

2. **Upgrade the deployment:**
   ```bash
   helm upgrade todo-app ./helm/todo-app
   ```

3. **Uninstall:**
   ```bash
   helm uninstall todo-app
   ```

### Using kubectl (Raw Manifests)

1. **Apply all manifests:**
   ```bash
   kubectl apply -f k8s/
   ```

2. **Check deployment status:**
   ```bash
   kubectl get pods -n todo-app
   kubectl get svc -n todo-app
   ```

## ArgoCD GitOps Deployment

1. **Apply the ArgoCD application:**
   ```bash
   kubectl apply -f argocd/application.yaml
   ```

2. **Apply the ArgoCD project (optional):**
   ```bash
   kubectl apply -f argocd/appproject.yaml
   ```

3. **Access ArgoCD UI and sync the application**

## Configuration

### Helm Values

Key configuration options in `helm/todo-app/values.yaml`:

- `replicaCount`: Number of pod replicas (default: 2)
- `image.repository`: Docker image repository
- `image.tag`: Docker image tag
- `persistence.enabled`: Enable SQLite data persistence (default: true)
- `persistence.size`: Storage size for SQLite database (default: 1Gi)
- `ingress.enabled`: Enable ingress (default: true)
- `ingress.hosts[0].host`: Hostname for the application (default: todo-app.local)

### Environment Variables

- `PORT`: Application port (default: 5000)

## API Endpoints

- `GET /` - Main todo application interface
- `POST /add` - Add a new todo
- `GET /toggle/<id>` - Toggle todo completion status
- `GET /delete/<id>` - Delete a todo
- `GET /api/todos` - Get all todos as JSON
- `GET /health` - Health check endpoint

## Database

The application uses SQLite for data storage with the following schema:

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     ArgoCD      │───▶│   Kubernetes    │───▶│   Todo App      │
│   (GitOps)      │    │     Cluster     │    │   (Flask)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                         │
                              ▼                         ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │      Helm       │    │     SQLite      │
                       │    (Charts)     │    │   (Database)    │
                       └─────────────────┘    └─────────────────┘
```

## Development

### Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container image definition
├── .dockerignore         # Docker ignore patterns
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   └── index.html        # Main page template
├── k8s/                  # Raw Kubernetes manifests
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── pvc.yaml
├── helm/                 # Helm chart
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
└── argocd/              # ArgoCD manifests
    ├── application.yaml
    └── appproject.yaml
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally and with Docker
5. Submit a pull request

## Security

- Application runs as non-root user in container
- Resource limits configured for pods
- Health checks implemented for reliability
- SQLite database stored in persistent volume

## Monitoring

The application provides a health check endpoint at `/health` that returns:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

## License

This project is licensed under the MIT License.
