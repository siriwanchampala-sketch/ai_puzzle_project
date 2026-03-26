from google import genai

# 👉 ใส่ API KEY
client = genai.Client(api_key="AIzaSyDHMvXhBKCdPkHlr9-UAArs2CLNFxE2RqQ")
def fallback_analysis(results):
    fastest = min(results, key=lambda x: results[x]["time"])
    least_steps = min(results, key=lambda x: results[x]["steps"])

    return f"""
📊 วิเคราะห์ (Fallback):

🔹 เร็วที่สุด: {fastest}
🔹 ก้าวน้อยสุด: {least_steps}

📌 วิเคราะห์:
- BFS: หา solution ได้แน่นอน แต่กิน memory สูง
- DFS: ใช้ memory น้อย แต่เสี่ยงไม่ optimal
- A*: ใช้ heuristic ทำให้เร็วและแม่น

🎯 สรุป:
- ถ้าต้องการความเร็ว → {fastest}
- ถ้าต้องการคำตอบดีที่สุด → A*
"""
def analyze(results):
    prompt = f"""
นี่คือผลลัพธ์ของ Search Algorithms:

{results}

ช่วยวิเคราะห์แบบละเอียด:

1. เปรียบเทียบเวลา (เร็ว/ช้า)
2. เปรียบเทียบจำนวนก้าว (optimal หรือไม่)
3. วิเคราะห์ข้อดีข้อเสียของ BFS, DFS, A*
4. อธิบายว่าแต่ละ algorithm เหมาะกับสถานการณ์แบบไหน
5. สรุปว่า algorithm ไหนดีที่สุด และเพราะอะไร

ตอบเป็นภาษาไทย แบบเข้าใจง่าย
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text

    except:
        # 🔥 👉 ตรงนี้คือจุดเรียก fallback
        return fallback_analysis(results)