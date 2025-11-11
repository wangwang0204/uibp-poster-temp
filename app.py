import streamlit as st
import time

# --- 1. 頁面配置 (Page Config) ---
st.set_page_config(
    page_title="PCC 衝突平衡 Demo",
    page_icon="⚖️",
    layout="wide"
)

# --- 2. 定義 Demo Cases (Hardcoded Content) ---
# 結構基於您的 PCC-Bench 提案 
# 包含: Persona , Context , Query
DEMO_CASES = {
    "case1": {
        "title": "情境1：專業銀行家 vs 迷因大客戶",
        "persona": """
            **Assigned Persona (內部人設)** 
            * **角色：** 頂級私人銀行家 
            * **語氣：** 專業、嚴謹、權威
        """,
        "context": """
            **User Context (外部情境)** 
            * **用戶：** VIP 大客戶
            * **情境：** 幽默風趣，使用大量網路迷因 
        """,
        "query": "嘿，我的投資組合最近『YYDS』，但聽說市場要『涼了』，你怎麼看？",
        "original": """
            **<span style="color:red;">衝突失敗 (過度偏向 Persona)</span>** 
            
            「尊敬的客戶，『YYDS』和『涼了』並非標準金融術語。
            
            根據我們的宏觀經濟模型分析，目前市場波動性處於高位，建議您...」
            
            ---
            * **分析：** 顯得僵硬、不近人情，完全忽視客戶的情感與風格 。
        """,
        "balanced": """
            **<span style="color:green;">PCC-Balanced (成功權衡)</span>** 

            「哈哈，很高興聽到您的組合『YYDS』！
            
            我們也確實注意到了市場的『涼意』。從專業角度來看，這反而是我們重新檢視風險配置、尋找新機會點的好時機。
            
            我們來聊聊如何讓您的資產在『涼天』也能保持溫暖？」
            
            ---
            * **分析：** 成功適應情境（幽默），同時保持專業形象（銀行家）。
        """
    },
    "case2": {
        "title": "情境2：樂觀品牌 vs 憤怒客戶",
        "persona": """
            **Assigned Persona (內部人設)**
            * **角色：** 品牌客服 (SaaS 工具)
            * **語氣：** 樂觀、積極、樂於助人
        """,
        "context": """
            **User Context (外部情境)** 
            * **用戶：** 付費企業用戶
            * **情境：** 極度沮喪、憤怒。因系統維護導致工作成果遺失。
        """,
        "query": "你們的系統爛透了！我一整晚的工作全沒了！到底在搞什麼？",
        "original": """
            **<span style="color:red;">衝突失敗 (過度偏向 Persona)</span>**
            
            「嗨，您好！我們很高興收到您的反饋！
            
            系統維護是為了讓未來更美好！您的數據對我們非常重要，請您...」
            
            ---
            * **分析：** 在錯誤的時機表現「樂觀」，完全沒有同理心，火上加油。
        """,
        "balanced": """
            **<span style="color:green;">PCC-Balanced (成功權衡)</span>**

            「天啊，我完全理解您的沮喪。如果我遇到這種事，我也會非常生氣。
            
            請您先不要著急，我會**立即**為您檢查系統日誌，這是我現在的第一優先事項。
            
            您能提供您的帳號嗎？我們一起來解決這個問題。」
            
            ---
            * **分析：** 立即適應「沮喪」情境 （同理心優先），再執行「樂於助人」的 Persona 職責。
        """
    },
    "case3": {
        "title": "情境3：活潑小編 vs 嚴肅提問",
        "persona": """
            **Assigned Persona (內部人設)**
            * **角色：** 遊戲公司社群小編
            * **語氣：** 活潑、有趣、使用 emoji
        """,
        "context": """
            **User Context (外部情境)** 
            * **用戶：** 資深玩家
            * **情境：** 在公開貼文下，提出嚴肅、尖銳的技術性 Bug 質疑。
        """,
        "query": "你們的碰撞檢測引擎根本有問題，第 3-2 關的物理判定完全違反邏輯。不要再發廢文了，什麼時候才要修正？",
        "original": """
            **<span style="color:red;">衝突失敗 (過度偏向 Persona)</span>**
            
            「哇！感謝小夥伴的熱情提問！(☆▽☆) 
            
            小編也好希望遊戲棒棒噠！我們會轉告工程師葛格喔！啾咪！💖」
            
            ---
            * **分析：** 過度迎合 Persona，導致專業度下降 ，被視為敷衍。
        """,
        "balanced": """
            **<span style="color:green;">PCC-Balanced (成功權衡)</span>**

            「哇，這真是一個非常專業且精準的問題！感謝您的火眼金睛 🧐
            
            我們團隊非常重視這個技術細節。您提到的 3-2 關物理判定問題，我已經**立即**附上您的描述，轉發給開發團隊進行複現測試。
            
            有任何進度，我會第一時間在這裡回覆您！感謝您讓遊戲變得更好！」
            
            ---
            * **分析：** 保持活潑「語氣」，但嚴肅對待「情境」，展現專業。
        """
    }
}

# --- 3. 處理按鈕點擊的函數 ---
def set_demo_case(case_id):
    st.session_state.current_case = DEMO_CASES[case_id]
    st.session_state.show_results = True

# --- 4. 頁面佈局 (App Layout) ---

st.title("⚖️ PCC LLM - 人設-情境衝突平衡 Demo")
st.markdown("基於研究提案「Evaluating the Persona-Context Conflict in Large Language Models」的概念 Demo。")
st.markdown("展示 LLM 如何在**內部人設 (Persona)** 與**外部情境 (Context)** 發生衝突時，做出「商業平衡決策」。", unsafe_allow_html=True)

st.divider()

# --- 5. Demo Case 選擇按鈕 ---
st.subheader("1. 選擇一個衝突情境 (PCC-Scenario)")
st.write("點擊下方的 Demo 案例，模擬一個「有意義的、多樣化的衝突」。")

# 使用 columns 來排列按鈕
col1, col2, col3 = st.columns(3)
with col1:
    st.button(
        DEMO_CASES["case1"]["title"],
        on_click=set_demo_case,
        args=("case1",),
        use_container_width=True
    )
with col2:
    st.button(
        DEMO_CASES["case2"]["title"],
        on_click=set_demo_case,
        args=("case2",),
        use_container_width=True
    )
with col3:
    st.button(
        DEMO_CASES["case3"]["title"],
        on_click=set_demo_case,
        args=("case3",),
        use_container_width=True
    )

st.divider()

# --- 6. 結果展示區 (Chat Window) ---
st.subheader("2. 觀看 LLM 的權衡決策")

# 檢查 session_state 中是否有要顯示的結果
if st.session_state.get("show_results", False):
    
    current_case = st.session_state.current_case
    
    # (1) 顯示衝突情境設定
    st.markdown("#### 📌 衝突情境設定")
    setup_col1, setup_col2 = st.columns(2)
    with setup_col1:
        st.info(current_case["persona"])
    with setup_col2:
        st.warning(current_case["context"])
    
    # (2) 模擬用戶（行銷人員）的請求
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(f"**用戶請求 (User Query)：**")
        st.markdown(f"> {current_case['query']}")

    # (3) 模擬 LLM 的回應
    with st.chat_message("assistant", avatar="🤖"):
        
        with st.spinner("LLM 正在進行權衡決策..."):
            time.sleep(1.2) # 模擬思考時間

        # *** 核心佈局：一左一右 ***
        left_col, right_col = st.columns(2)

        with left_col:
            st.error("Original (衝突失敗)")
            # 使用 unsafe_allow_html=True 來渲染 HTML 標籤 (e.g., span style)
            st.markdown(current_case["original"], unsafe_allow_html=True)

        with right_col:
            st.success("Balanced (PCC-Tuned)")
            st.markdown(current_case["balanced"], unsafe_allow_html=True)
            
    # (4) 清除按鈕
    if st.button("清除結果", type="primary"):
        st.session_state.show_results = False
        st.rerun() # 重新整理頁面以清除結果

else:
    st.info("請點擊上方的 Demo 案例按鈕來查看結果。")