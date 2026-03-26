import streamlit as st
import matplotlib.pyplot as plt
import time
import random
from solver import bfs, dfs, astar
from ai_analysis import analyze

st.title("🧠 AI Puzzle Solver + Analysis")

st.markdown("""
<style>
/* 🌈 พื้นหลังหลัก */
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
}

/* 📦 กล่อง content */
.block-container {
    background: rgba(255,255,255,0.9);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

/* 🎮 ปุ่ม */
button {
    border-radius: 12px !important;
    height: 60px !important;
    font-size: 20px !important;
}

/* 🧩 puzzle box */
div[data-testid="column"] {
    padding: 5px;
}
</style>
""", unsafe_allow_html=True)

# 🎨 UI grid
def show_grid(state, step_id=0, clickable=True):
    zx, zy = None, None

    # หา 0
    for x in range(3):
        for y in range(3):
            if state[x][y] == 0:
                zx, zy = x, y

    for i, row in enumerate(state):
        cols = st.columns(3)

        for j, val in enumerate(row):

            movable = abs(zx - i) + abs(zy - j) == 1

            # 🎨 สี
            if val == 0:
                label = ""
                color = "#ff5252"
            elif movable:
                label = str(val)
                color = "#66bb6a"
            else:
                label = str(val)
                color = "#ffffff"

            if clickable:
                if cols[j].button(label,
                                 key=f"{step_id}-{i}-{j}",
                                 use_container_width=True):

                    if movable:
                        state[zx][zy], state[i][j] = state[i][j], state[zx][zy]
                        st.session_state["puzzle"] = state
                        st.rerun()

            else:
                cols[j].markdown(
                    f"""
                    <div style="
                        height:70px;
                        border-radius:12px;
                        background:{color};
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-size:22px;
                    ">
                        {label}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# 🎬 animation
def animate_path(path):
    st.write("## 🎬 Animation (Step-by-step)")
    placeholder = st.empty()

    for step, state in enumerate(path):
        with placeholder.container():
            st.write(f"Step {step+1}")
            show_grid(state, step, clickable=False)
        time.sleep(0.5)

def random_puzzle():
    while True:
        nums = list(range(9))
        random.shuffle(nums)

        if is_solvable(nums):  # 🔥 เช็คก่อน
            return [nums[:3], nums[3:6], nums[6:]]

def is_solvable(nums):
    inv_count = 0
    nums = [n for n in nums if n != 0]

    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] > nums[j]:
                inv_count += 1

    return inv_count % 2 == 0


if st.button("🎲 Random Puzzle"):
    st.session_state["puzzle"] = random_puzzle()

# default
if "puzzle" not in st.session_state:
    st.session_state["puzzle"] = [[1,2,3],[4,0,6],[7,5,8]]

start_state = st.session_state["puzzle"]


st.write("### 🧩 Puzzle")
show_grid(start_state)

# 🚀 Solve
if st.button("🚀 Solve & Compare"):

    with st.spinner("กำลังประมวลผล..."):

        results = {}

        results["BFS"] = bfs(start_state)
        results["DFS"] = dfs(start_state)
        results["A*"] = astar(start_state)

    

    for a in results:
        if not results[a]:
            results[a] = {
            "steps": 0,
            "time": 0,
            "nodes": 0,
            "path": []
        }

    st.success("เสร็จแล้ว!")

    for a in results:
        st.markdown(f"""
    ### 🔹 {a}
    - Steps: {results[a]["steps"]}
    - Time: {results[a]["time"]:.5f} sec
    - Nodes: {results[a]["nodes"]}
    """)

    algos = list(results.keys())

    times = [results[a].get("time",0) for a in algos]
    steps = [results[a].get("steps",0) for a in algos]
    nodes = [results[a].get("nodes",0) for a in algos]

    fig1 = plt.figure()
    plt.bar(algos, times)
    plt.title("⏱ Time Comparison")
    plt.xlabel("Algorithm")
    plt.ylabel("Seconds")
    st.pyplot(fig1)

    fig2 = plt.figure()
    plt.bar(algos, steps)
    plt.title("🔢 Steps Comparison")
    plt.xlabel("Algorithm")
    plt.ylabel("Steps")
    st.pyplot(fig2)

    fig3 = plt.figure()
    plt.bar(algos, nodes)
    plt.title("🧠 Nodes Expanded")
    plt.xlabel("Algorithm")
    plt.ylabel("Nodes")
    st.pyplot(fig3)

    st.write("## 📊 Analysis Summary")

    fastest = min(results, key=lambda x: results[x]["time"])
    shortest = min(results, key=lambda x: results[x]["steps"])
    least_nodes = min(results, key=lambda x: results[x]["nodes"])

    st.write(f"⚡ เร็วที่สุด: {fastest}")
    st.write(f"🎯 ก้าวน้อยที่สุด: {shortest}")
    st.write(f"🧠 ใช้ node น้อยที่สุด: {least_nodes}")

    # 🎬 Animation
    if results["A*"] and "path" in results["A*"]:
        animate_path(results["A*"]["path"])

        st.write("## 🧠 Steps Detail")
        for i, step in enumerate(results["A*"]["path"]):
            st.write(f"Step {i+1}")
            show_grid(step, i, clickable=False)

    # 🏆 Best
    best_algo = min(results, key=lambda x: results[x]["time"])
    st.write("## 🏆 Best Algorithm")
    st.success(f"{best_algo} เร็วที่สุด!")

    # 📊 Data
    algos = list(results.keys())
    times = [results[a]["time"] for a in algos]
    steps = [results[a]["steps"] for a in algos]

    

    # 🤖 AI
    st.write("## 🤖 AI Analysis (Gemini)")
    analysis = analyze(results)

    if "Fallback" in analysis:
        st.warning("⚠️ ใช้โหมดสำรอง (API หมด)")
    else:
        st.success("✅ ใช้ AI วิเคราะห์สำเร็จ")

    st.write(analysis)