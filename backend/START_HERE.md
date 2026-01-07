# 🎯 START HERE: PostgreSQL + Adminer Setup

## What You Asked For

You wanted to:
1. ✅ **Switch from SQLite to PostgreSQL**
2. ✅ **Use Adminer (like phpMyAdmin) to manage your database**

## What's Been Done

I've created everything you need:
- ✅ Added Adminer to docker-compose.yml
- ✅ Created automated migration script
- ✅ Created comprehensive documentation
- ✅ Made it super easy to set up

---

## 🚀 Quick Setup (2 Commands)

### Step 1: Go to backend directory
```bash
cd backend
```

### Step 2: Run the setup script
```bash
bash scripts/quick_postgres_setup.sh
```

**That's it!** The script will:
1. Start PostgreSQL and Adminer
2. Update your .env file
3. Run database migrations
4. Copy all your data from SQLite to PostgreSQL
5. Verify everything works

**Time:** 2-3 minutes  
**Your data:** Safely preserved (SQLite file stays as backup)

---

## 🌐 After Setup - Access Your Database

### Option 1: Adminer (Visual Interface) ⭐ RECOMMENDED

1. **Open browser:** http://localhost:8080

2. **Login with:**
   ```
   System: PostgreSQL
   Server: postgres
   Username: agrisense_user
   Password: changeme
   Database: agrisense
   ```

3. **Click "Login"**

4. **You'll see:**
   - 📊 All your tables (users, sensor_readings, pest_detections, alerts)
   - ✏️ Edit any record with a click
   - ➕ Add new records with a form
   - 🗑️ Delete records easily
   - 🔍 Run SQL queries with syntax highlighting
   - 📥 Export data to CSV/SQL/JSON
   - 📤 Import data from files

### Option 2: PostgreSQL CLI (For Advanced Users)
```bash
docker exec -it agrisense-postgres psql -U agrisense_user -d agrisense
```

---

## 📊 What You'll See in Adminer

After logging in, click on each table:

### 1. **users** table
- 3 users (admin, farmer1, farmer2)
- Columns: id, username, hashed_password, is_active, created_at

### 2. **sensor_readings** table
- 504 readings (7 days of hourly data for 3 users)
- Columns: id, user_id, temperature, humidity, soil_moisture, light_intensity, timestamp

### 3. **pest_detections** table
- 9 detections (Fall Armyworm, Aphids, Whitefly)
- Columns: id, user_id, image_url, pest_type, confidence, severity, recommendations, detected_at

### 4. **alerts** table
- 12 alerts (weather, pest, environmental)
- Columns: id, user_id, alert_type, title, message, severity, is_read, created_at

---

## 🎨 Cool Things You Can Do in Adminer

### 1. Browse and Filter Data
- Click any table
- Use the filter boxes at the top
- Sort by clicking column headers

### 2. Edit Records
- Click "edit" next to any record
- Change values in the form
- Click "Save"

### 3. Run SQL Queries
Click "SQL command" and try these:

```sql
-- Get all users
SELECT * FROM users;

-- Get sensor readings from last 24 hours
SELECT * FROM sensor_readings 
WHERE timestamp > NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC;

-- Get high-confidence pest detections
SELECT * FROM pest_detections 
WHERE confidence > 0.8
ORDER BY detected_at DESC;

-- Get unread alerts
SELECT * FROM alerts 
WHERE is_read = false
ORDER BY created_at DESC;

-- Get average temperature by user
SELECT u.username, AVG(s.temperature) as avg_temp
FROM users u
LEFT JOIN sensor_readings s ON u.id = s.user_id
GROUP BY u.username;
```

### 4. Export Data
- Click "Export" in left menu
- Choose format (SQL, CSV, JSON)
- Click "Export"
- Download file

### 5. Import Data
- Click "Import" in left menu
- Choose file
- Click "Execute"

---

## 🧪 Test Your Setup

### 1. Check Backend Connection
```bash
curl http://localhost:5000/health
```

Should show:
```json
{
  "status": "healthy",
  "database": "connected",
  "database_type": "postgresql"
}
```

### 2. Test API
Open: http://localhost:5000/docs

Try:
- POST /api/v1/auth/login (username: admin, password: admin123)
- GET /api/v1/sensor/ (requires auth token)

### 3. Check Data in Adminer
1. Go to http://localhost:8080
2. Login with credentials above
3. Click "users" → Should see 3 users
4. Click "sensor_readings" → Should see 504 readings

---

## 🔄 Useful Commands

### Start PostgreSQL and Adminer
```bash
docker-compose up -d postgres adminer
```

### Stop Everything
```bash
docker-compose down
```

### View PostgreSQL Logs
```bash
docker-compose logs -f postgres
```

### Restart PostgreSQL
```bash
docker-compose restart postgres
```

### Backup Database
```bash
docker exec -t agrisense-postgres pg_dump -U agrisense_user agrisense > backup.sql
```

### Restore Database
```bash
cat backup.sql | docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense
```

---

## 🐛 Troubleshooting

### "Connection refused"
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Wait 10 seconds
sleep 10
```

### "Can't access Adminer"
```bash
# Make sure it's running
docker-compose ps adminer

# If not, start it
docker-compose up -d adminer
```

### "Wrong password"
Make sure you're using:
- Username: `agrisense_user`
- Password: `changeme`
- Server: `postgres` (not localhost)

### "Empty database"
```bash
# Run migrations
cd backend
alembic upgrade head

# Migrate data
python scripts/migrate_sqlite_to_postgres.py
```

---

## 📚 Documentation Files

If you need more details:

1. **QUICK_START_POSTGRESQL.md** - 5-minute quick start
2. **POSTGRESQL_SETUP.md** - Detailed 486-line guide
3. **DATABASE_MIGRATION_SUMMARY.md** - Overview and comparison

---

## ✅ Checklist

After running the setup script, verify:

- [ ] PostgreSQL running: `docker-compose ps postgres` shows "Up (healthy)"
- [ ] Adminer running: `docker-compose ps adminer` shows "Up"
- [ ] Can access Adminer: http://localhost:8080
- [ ] Can login to Adminer with credentials
- [ ] See 4 tables: users, sensor_readings, pest_detections, alerts
- [ ] Backend health check shows "postgresql": http://localhost:5000/health
- [ ] API docs work: http://localhost:5000/docs
- [ ] Can login with admin/admin123

---

## 🎉 You're Done!

You now have:
- ✅ **PostgreSQL** running (production-grade database)
- ✅ **Adminer** running (visual database manager)
- ✅ **All your data** migrated from SQLite
- ✅ **Easy access** to manage your database

**Next:** Open http://localhost:8080 and explore your data!

---

## 🆘 Need Help?

If something doesn't work:

1. Check if Docker is running: `docker ps`
2. Check PostgreSQL logs: `docker-compose logs postgres`
3. Check Adminer logs: `docker-compose logs adminer`
4. Read the troubleshooting section above
5. Check the detailed guides in the documentation files

---

**Setup Time:** 2-3 minutes  
**Difficulty:** Easy (automated)  
**Status:** Ready to use! 🚀
