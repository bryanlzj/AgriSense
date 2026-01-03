# Development Environment Notes

## 🏗️ Current Environment: Evo Builder

**What is Evo Builder?**
- Online IDE environment for React + .NET projects
- Primarily designed for full-stack web applications
- **Does NOT have Python installed** (this is expected)

---

## 🎯 AgriSense Development Strategy

Since AgriSense is a **Flutter Mobile App + FastAPI Backend** project, the development will be split:

### **What We're Doing in Evo Builder:**
✅ **Project Planning & Documentation**
- Creating PRD (Product Requirements Document)
- Creating Task Lists
- Creating API specifications
- Creating database schemas
- Writing backend code files (Python/FastAPI)
- Writing mobile app code files (Flutter/Dart)

✅ **Code Generation**
- All backend Python files
- All mobile Flutter files
- Configuration files
- Documentation

❌ **What We CANNOT Do in Evo Builder:**
- Run Python/FastAPI backend (no Python installed)
- Run Flutter mobile app (no Flutter SDK installed)
- Test the actual application
- Install Python/Flutter dependencies

---

## 💻 Your Local Development Environment

You will need to set up your **local machine** or **your own server** with:

### **Backend Requirements:**
```bash
# Install Python 3.10+
python3 --version

# Create virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn main:app --reload --port 5000
```

### **Mobile Requirements:**
```bash
# Install Flutter SDK
flutter --version

# Get dependencies
cd mobile
flutter pub get

# Run on emulator/device
flutter run
```

### **Database:**
```bash
# Option 1: SQLite (Development - Easiest)
# No installation needed, just works!

# Option 2: PostgreSQL (Production)
# Install PostgreSQL locally or use Docker
docker run --name agrisense-db -e POSTGRES_PASSWORD=yourpassword -p 5432:5432 -d postgres
```

---

## 🔄 Development Workflow

### **Phase 1: Code Generation (Evo Builder)** ← **We are here**
1. ✅ Create all project files
2. ✅ Write all backend code
3. ✅ Write all mobile code
4. ✅ Generate documentation
5. ✅ Create configuration files

### **Phase 2: Local Development (Your Machine)**
1. Clone/download the generated code
2. Set up Python virtual environment
3. Install backend dependencies
4. Set up Flutter SDK
5. Install mobile dependencies
6. Run and test locally

### **Phase 3: Deployment (Your Server)**
1. Deploy backend to your server (Docker recommended)
2. Set up PostgreSQL database
3. Configure environment variables
4. Build Flutter APK
5. Test on real Android device

---

## 📝 Task Completion Strategy

For tasks that require **running code** (like Task 0.2.2):

✅ **In Evo Builder:**
- Generate all necessary files
- Write complete, production-ready code
- Document setup instructions
- Mark task as complete with notes

✅ **In Your Local Environment:**
- Follow the documented instructions
- Actually run and test the code
- Verify everything works
- Report any issues back

---

## 🎯 Current Status

**Tasks Completed in Evo Builder:**
- ✅ 0.1.1: Project directory structure
- ✅ 0.1.2: Git repository
- ✅ 0.1.3: README.md
- ✅ 0.2.1: FastAPI project structure (all files created)
- ✅ 0.2.2: Virtual environment setup (instructions documented)

**Next Tasks:**
- 0.2.3: Database configuration (will generate code)
- 0.3.x: Database models (will generate code)
- 1.x.x: API endpoints (will generate code)

---

## 💡 Key Insight

**Evo Builder is your CODE GENERATOR.**  
**Your local machine is your RUNTIME ENVIRONMENT.**

This is actually a **good separation of concerns**:
- Evo Builder = Fast, AI-assisted code generation
- Local machine = Testing and debugging
- Your server = Production deployment

---

## ✅ Action Items for You

When you're ready to actually **run** the backend:

1. **Copy all files from `/backend` folder** to your local machine
2. **Run the setup commands** documented in each task
3. **Test the endpoints** using the Swagger UI at `http://localhost:5000/swagger`
4. **Report any issues** and we'll fix the code here in Evo Builder

---

**This approach lets us move FAST on code generation while you handle the actual runtime testing!** 🚀
