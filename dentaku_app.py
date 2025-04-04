import streamlit as st
import re

def setup_page():
    st.set_page_config(
        page_title="電卓",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    st.markdown("""
        <style>
        .stApp {
            /* 背景色や全体の文字色はお好みで調整してください */
             background-color: white; 
             color: black; 
        }
        .stButton>button {
            width: 100%; /* 列幅いっぱいに広げる */
            height: 60px;
            margin: 4px 0; /* 上下のマージンを調整 */
            font-size: 20px;
            border-radius: 5px; /* 角を少し丸める */
            background-color: white;
            color: black;
            border: 1px solid #ccc; /* 枠線を追加 */

        }
        .display-area {
            background-color: #f0f0f0; /* 表示エリア背景色 */
            color: black; /* 表示エリア文字色 */
            padding: 15px;
            margin: 15px 0;
            font-size: 28px; /* フォントサイズを大きく */
            text-align: right;
            min-height: 60px;
            border-radius: 5px;
            font-family: 'Courier New', Courier, monospace; /* 等幅フォント */
            overflow-x: auto; /* 横スクロールを可能に */
            white-space: nowrap; /* 折り返しを防ぐ */
            border: 1px solid #ccc; /* 枠線を追加 */
        }
        /* =ボタンの色を変える例 */
        .stButton:nth-child(15) > button { /* = Button の位置を確認して調整 */
            background-color: #4CAF50;
            color: white;
        }
        /* AC, Cボタンの色を変える例 */
        .stButton:nth-child(11) > button, /* C Button の位置 */
        .stButton:nth-child(16) > button { /* AC Button の位置 */
            background-color: #f44336;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

def evaluate_expression(expression):
    # eval() はセキュリティリスクがあるため注意が必要です。
    # 入力される可能性のある文字を制限するなど、より安全な方法を検討してください。
    try:
        # 表示用の記号を計算用の記号に置換
        expression_to_eval = expression.replace('×', '*').replace('÷', '/')

        # 不正な文字がないか基本的なチェック
        if not re.fullmatch(r'^[0-9\.\+\-\*\/()\s]*$', expression_to_eval):
             return "エラー: 不正文字"
        # 式が空、または演算子で終わっている場合は評価しない
        if not expression_to_eval or expression_to_eval[-1] in ['+', '-', '*', '/']:
             # return expression # そのまま表示を返すか、エラーにするか
             return "エラー: 式不完全"

        result = eval(expression_to_eval)

        # 結果が整数なら整数で、小数なら適切な桁数で表示
        if isinstance(result, (int, float)):
            if result == int(result):
                return str(int(result))
            else:
                # 小数点以下の不要な0を削除 (例: 12.3400 -> 12.34)
                return f"{result:.10f}".rstrip('0').rstrip('.')
        else:
            return "エラー: 計算不能" # 複素数などが返る場合
    except ZeroDivisionError:
        return "エラー: 0除算"
    except SyntaxError:
        return "エラー: 式の誤り"
    except Exception as e:
        print(f"評価エラー: {e}") # ログに詳細を出力
        return "エラー"

def main():
    setup_page()

    # セッションステートで表示内容を管理
    if 'display' not in st.session_state:
        st.session_state.display = ""

    st.title("電卓")

    # 表示エリア (st.markdown を使用)
    st.markdown(f'<div class="display-area">{st.session_state.display}</div>', unsafe_allow_html=True)
    # --- 代替案: st.text_input を使う場合 ---
    # st.text_input("Display", st.session_state.display, key="display_input", disabled=True, label_visibility="collapsed")
    # この場合、上記の display-area のCSSは不要になるか、text_input 用に調整が必要です。

    # ボタンの配置
    col1, col2, col3, col4 = st.columns(4)

    # --- ボタン処理: 各ボタンのif文の中に st.rerun() を追加 ---
    with col1:
        if st.button("("):
            st.session_state.display += "("
            st.rerun() # <<< 追加
        if st.button("7"):
            st.session_state.display += "7"
            st.rerun() # <<< 追加
        if st.button("4"):
            st.session_state.display += "4"
            st.rerun() # <<< 追加
        if st.button("1"):
            st.session_state.display += "1"
            st.rerun() # <<< 追加
        if st.button("0"):
            st.session_state.display += "0"
            st.rerun() # <<< 追加

    with col2:
        if st.button(")"):
            st.session_state.display += ")"
            st.rerun() # <<< 追加
        if st.button("8"):
            st.session_state.display += "8"
            st.rerun() # <<< 追加
        if st.button("5"):
            st.session_state.display += "5"
            st.rerun() # <<< 追加
        if st.button("2"):
            st.session_state.display += "2"
            st.rerun() # <<< 追加
        if st.button("."):
            # 簡単なドット入力制御（最後の数値にドットが含まれていない場合のみ追加）
            current_number = ""
            for char in reversed(st.session_state.display):
                if char.isdigit() or char == '.':
                    current_number += char
                else:
                    break
            current_number = current_number[::-1] # 逆順を元に戻す

            if '.' not in current_number:
                 # 最初や演算子の後にドットを押した場合 '0.' とする
                 if not st.session_state.display or st.session_state.display[-1] in '+-×÷(':
                     st.session_state.display += "0."
                 else:
                     st.session_state.display += "."
                 st.rerun() # <<< 追加
            # すでにドットがある場合は何もしない（rerunもしない）

    with col3:
        if st.button("C"): # Clear Entry (最後の一文字削除)
            # エラーメッセージが表示されている場合は全削除(ACと同じ動作)にする
            if st.session_state.display.startswith("エラー"):
                st.session_state.display = ""
            else:
                st.session_state.display = st.session_state.display[:-1]
            st.rerun() # <<< 追加
        if st.button("9"):
            st.session_state.display += "9"
            st.rerun() # <<< 追加
        if st.button("6"):
            st.session_state.display += "6"
            st.rerun() # <<< 追加
        if st.button("3"):
            st.session_state.display += "3"
            st.rerun() # <<< 追加
        if st.button("="):
            # 式が空でない場合のみ評価
            if st.session_state.display:
                st.session_state.display = evaluate_expression(st.session_state.display)
                st.rerun() # <<< 追加
            # 空の場合は何もしない

    with col4:
        if st.button("AC"): # All Clear
            st.session_state.display = ""
            st.rerun() # <<< 追加
        # 演算子ボタン (簡単に入力が空でない＆最後が演算子でない場合に追加)
        if st.button("÷"):
            if st.session_state.display and st.session_state.display[-1] not in '+-×÷(':
                st.session_state.display += "÷"
                st.rerun() # <<< 追加
        if st.button("×"):
            if st.session_state.display and st.session_state.display[-1] not in '+-×÷(':
                st.session_state.display += "×"
                st.rerun() # <<< 追加
        if st.button(""-""):
             # マイナスは数字や括弧の後、または式の先頭で許可する例
            if st.session_state.display and st.session_state.display[-1] not in '+-×÷(':
                 st.session_state.display += "-"
                 st.rerun() # <<< 追加
            elif not st.session_state.display or st.session_state.display[-1] == '(': # 先頭や括弧の後
                 st.session_state.display += "-"
                 st.rerun() # <<< 追加
        if st.button("+"):
            if st.session_state.display and st.session_state.display[-1] not in '+-×÷(':
                st.session_state.display += "+"
                st.rerun() # <<< 追加

if __name__ == "__main__":
    main()