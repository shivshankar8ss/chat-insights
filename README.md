# 📊 Chat Insights — WhatsApp Chat Analyzer

Chat Insights is a powerful **WhatsApp Chat Analyzer** built with Python and Streamlit.  
It processes exported WhatsApp chats and provides **detailed visualizations**, **sentiment analysis**, and **chat activity trends**.

---

## 🚀 Features
- 📅 **Daily, Monthly & Hourly Activity Analysis**
- 😀 **Emoji usage statistics**
- 🗣 **Most active participants**
- 📈 **Message frequency trends**
- 🔥 **Activity heatmaps**
- 📝 **Word frequency analysis**
- 💬 **Sentiment analysis** (positive, neutral, negative)
- 🌐 **Works on group or personal chats**

---

## 📂 How to Export Your WhatsApp Chat
1. Open WhatsApp and go to the chat you want to analyze.  
2. Tap the **three dots (⋮)** in the top-right corner.  
3. Select **More** → **Export chat**.  
4. Choose **Without Media** (recommended for faster analysis).  
5. Save the `.txt` file or send it to your email.  

💡 **Tip:** Use the `.txt` file directly from WhatsApp without editing for the best results.

---

## 🛠 Installation & Setup (Local)
```bash
# Clone the repository
git clone https://github.com/your-username/chat-insights.git
cd chat-insights

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
