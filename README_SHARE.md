# 🏆 Concierge.com - Personal Life Management Platform

## 🚀 Quick Start

### Option 1: Run with Python
```bash
python run_concierge.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py --server.port=8501
```

## 🌐 Access the App
Open your browser and go to: **http://localhost:8501**

## 🎯 Features

### **Multi-Tier Service Plans:**
- **Basic Plan:** Self-service tools + email support
- **Premium Plan:** Personal concierge (Sarah Johnson) + AI insights  
- **Elite Plan:** 24/7 elite concierge (Michael Chen) + AI Command Center

### **AI-Powered Services:**
- **6 Specialized AI Agents:** Expense, Travel, Medical, Insurance, Tax, Communication
- **Intelligent Messaging:** Context-aware AI responses
- **Automated Task Management:** AI handles routine tasks
- **Performance Analytics:** Real-time AI agent monitoring

### **Life Management Services:**
- **💰 Expense Tracking:** AI-powered budget optimization
- **✈️ Travel Planning:** Concierge booking assistance
- **🏥 Medical Management:** Appointment scheduling
- **🛡️ Insurance Coordination:** Claims processing
- **📊 Tax Preparation:** AI assistance

### **Messaging System:**
- **Multi-channel communication:** Concierge, AI Agent, Support
- **Real-time message history** with read/unread status
- **Priority messaging** for Premium/Elite users
- **AI-powered responses** that understand context

## 🧪 Testing the App

1. **Sign up** with any plan (Basic, Premium, Elite)
2. **Test messaging:** Click "💬 New Message" in sidebar
3. **Try AI agents:** Send messages to "AI Agent" channel
4. **Explore services:** Navigate through different service tabs
5. **Test persistence:** Refresh page - messages should persist!

## 🔧 Debug Features

- **Quick Test Message:** Button on main dashboard
- **Debug Info Panel:** Expandable sidebar section
- **Message Count Display:** Real-time message tracking
- **System Status:** AI agent performance monitoring

## 📱 Demo Accounts

**Basic Plan:** Self-service tools
**Premium Plan:** Personal concierge (Sarah Johnson)  
**Elite Plan:** 24/7 elite concierge (Michael Chen)

## 🎯 How It Works

This app demonstrates how AI agents can scale human concierge services:

1. **AI First Response:** AI agents handle 80% of initial inquiries
2. **Human Escalation:** Complex requests go to human concierges  
3. **Seamless Handoff:** Smooth transitions between AI and human support
4. **Context Awareness:** Full conversation history and user preferences

## 🚀 Sharing Options

### **Local Network:**
```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```
Share: `http://YOUR_IP:8501`

### **Public Access (ngrok):**
```bash
# Install ngrok: brew install ngrok
# Run app: streamlit run app.py --server.port=8501
# In another terminal: ngrok http 8501
```

### **Streamlit Cloud:**
1. Push to GitHub
2. Deploy at [share.streamlit.io](https://share.streamlit.io)
3. Get public URL like `https://your-app.streamlit.app`

---

**Built with:** Streamlit, Python, AI Agents, Messaging System
**Contact:** support@concierge.com
