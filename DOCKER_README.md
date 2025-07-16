# 🐳 Docker Setup for YOLO Detection Django App

This Docker setup solves the Python 3.13 compatibility issues by using Python 3.11 in a containerized environment.

## 🚀 Quick Start with Docker

### Prerequisites
- Docker installed: https://docs.docker.com/get-docker/
- Docker Compose installed: https://docs.docker.com/compose/install/

### Option 1: Automated Setup (Recommended)
```bash
./docker-setup.sh
```

### Option 2: Manual Docker Setup
```bash
# Build the Docker image
docker-compose build

# Start the application
docker-compose up
```

### Option 3: Docker Commands Only
```bash
# Build image
docker build -t yolo-detection .

# Run container
docker run -p 8000:8000 -v $(pwd)/media:/app/media -v $(pwd)/yolo11n.pt:/app/yolo11n.pt yolo-detection
```

## 📁 What's Included

### Dockerfile
- **Python 3.11**: Compatible with PyTorch
- **System Dependencies**: OpenCV and other required libraries
- **PyTorch Installation**: From official source
- **Django Setup**: All Python dependencies
- **Volume Mounts**: For persistent data

### docker-compose.yml
- **Service Configuration**: YOLO detection app
- **Port Mapping**: 8000:8000
- **Volume Mounts**: 
  - `./media:/app/media` (uploads and results)
  - `./yolo11n.pt:/app/yolo11n.pt` (model file)
- **Environment Variables**: Django settings
- **Database Option**: PostgreSQL (commented out)

## 🎯 Benefits of Docker Setup

✅ **No Python Version Issues**: Uses Python 3.11  
✅ **Consistent Environment**: Same setup everywhere  
✅ **Easy Deployment**: One command to run  
✅ **Isolated Dependencies**: No conflicts with local Python  
✅ **Persistent Data**: Uploads and results saved locally  
✅ **Scalable**: Easy to add more services  

## 🔧 Docker Commands

### Build and Run
```bash
# Build the image
docker-compose build

# Start the application
docker-compose up

# Run in background
docker-compose up -d

# Stop the application
docker-compose down
```

### Development Mode
```bash
# Run with live reload (for development)
docker-compose -f docker-compose.dev.yml up
```

### Production Mode
```bash
# Run with production settings
docker-compose -f docker-compose.prod.yml up
```

### Debugging
```bash
# Access container shell
docker-compose exec yolo-detection bash

# View logs
docker-compose logs -f

# Rebuild without cache
docker-compose build --no-cache
```

## 📊 File Structure in Docker

```
/app/
├── detection/           # Django app
├── yolo_detection/     # Django settings
├── templates/          # HTML templates
├── static/            # Static files
├── media/             # Mounted volume (uploads/results)
├── yolo11n.pt         # Mounted model file
└── manage.py          # Django management
```

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8001:8000"  # Use port 8001 instead
   ```

2. **Permission issues**:
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER media/
   ```

3. **Model file not found**:
   ```bash
   # Ensure yolo11n.pt is in project root
   ls -la yolo11n.pt
   ```

4. **Build fails**:
   ```bash
   # Rebuild without cache
   docker-compose build --no-cache
   ```

### Performance Tips

- **GPU Support**: Add GPU support to Dockerfile
- **Multi-stage Build**: Optimize image size
- **Volume Caching**: Cache model files
- **Resource Limits**: Set memory/CPU limits

## 🚀 Production Deployment

### Using Docker Compose
```bash
# Production compose file
docker-compose -f docker-compose.prod.yml up -d
```

### Using Docker Swarm
```bash
# Deploy to swarm
docker stack deploy -c docker-compose.yml yolo-detection
```

### Using Kubernetes
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

## 🔧 Customization

### Environment Variables
```bash
# Add to docker-compose.yml
environment:
  - DEBUG=False
  - SECRET_KEY=your-secret-key
  - DATABASE_URL=postgresql://user:pass@db:5432/db
```

### Volume Mounts
```bash
# Add additional volumes
volumes:
  - ./logs:/app/logs
  - ./models:/app/models
```

### Network Configuration
```bash
# Custom network
networks:
  - yolo-network
```

## 📈 Monitoring

### Health Checks
```bash
# Add health check to Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1
```

### Logging
```bash
# View application logs
docker-compose logs -f yolo-detection

# View specific service logs
docker-compose logs -f --tail=100 yolo-detection
```

## 🎯 Next Steps

1. **Start the application**: `./docker-setup.sh`
2. **Access the web interface**: http://localhost:8000
3. **Upload an image**: Test the detection functionality
4. **Customize**: Modify Dockerfile for your needs
5. **Deploy**: Use in production environment

---

**Ready to detect objects with Docker! 🐳🎯** 