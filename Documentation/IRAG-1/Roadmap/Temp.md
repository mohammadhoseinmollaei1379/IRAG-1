### **Step 1: Start Infrastructure (Weaviate + TEI)**

powershell

Copy

```powershell
# Start the 2 core services (detached mode)
docker compose up weaviate embed -d

# Monitor model download progress (wait until you see "Ready" message)
docker compose logs -f embed
```

**Wait 3-5 minutes** until you see:

`INFO text_embeddings_router:server started: 0.0.0.0:8080`

Press `Ctrl+C` to exit logs.

---

### **Step 2: Verify Services are Healthy**

powershell

Copy

```powershell
# Check both services are running
docker compose ps

# Should show:
# NAME         STATUS
# farsi-rag-mvp-weaviate-1   Up (healthy)
# farsi-rag-mvp-embed-1      Up (healthy)
```

---

### **Step 3: Build Your App Container**

powershell

Copy

```powershell
# Build the Dockerfile (first time ~2-3 minutes)
docker compose build app
```

---

### **Step 4: Run Your Application**

powershell

Copy

```powershell
# Run the complete stack (infra + app)
docker compose up app
```

**The app will:**

1. Load documents from `data\raw_data\`
    
2. Send them to the Embedding service (TEI)
    
3. Store embeddings in Weaviate
    
4. Execute your query
    
5. Print the response and exit
    

---

### **Step 5: For Development (Run Repeatedly)**

After initial setup, just run:

powershell

Copy

```powershell
# To re-run the app after code changes:
docker compose up --build app  # Rebuilds if you changed requirements.txt or mvp.py

# To stop everything:
docker compose down

# To see logs if something breaks:
docker compose logs weaviate
docker compose logs embed
docker compose logs app
```

---

### **Troubleshooting Commands**

powershell

Copy

```powershell
# If services won't start:
docker compose down -v  # WARNING: Deletes all data
docker compose up -d weaviate embed

# If app says "connection refused":
# Wait 30 seconds and retry - TEI needs time to start

# Check disk space used by model:
docker system df -v
```

**Key point**: Model downloads **once** and persists in Docker volumes until you run `docker compose down -v`.