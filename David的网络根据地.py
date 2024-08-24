import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import requests, json

def fr_page():
    st.markdown("# Recommendation")
    with open('traced.ogg', 'rb') as f:
        test_ogg = f.read()
    st.audio(test_ogg, format='audio/ogg', start_time=0)
    copyright_media = ':blue[audio from the game Hacknet]'
    st.write(copyright_media)
    st.video("https://www.hacknet-os.com/Images/LinedTitle.webm")
    st.markdown("## Hacknet")
    st.markdown("### So What is Hacknet?")
    instruction = '''
    Hacknet is a modern, super immersive terminal-driven hacking game with a fully internally-consistent network simulation and an interface so real you shouldn't play it in an airport.
It follows the story of recently deceased hacker "Bit", whose death may not be the 'accident' the media reports.

You stand in for no one, as most games have you do - play for yourself, make your own decisions, and see the world react - if you're leaving a trace that is.
Hacknet has no protagonist, other than the person using it. Don't be reckless though - it's more real than you think.
'''
    st.markdown(instruction)
    links = ":blue[[Want more about it?](https://hacknet-os.com/)]"
    st.write(links)
    positive_fb = ":green[Thanks!]"
    negative_fb = ":green[Thank for your feedback. We'll imporve our product.]"
    command = st.text_input("Like or dislike?")
    if command == "like" or command == "Like":
        st.write(positive_fb)
    elif command == "dislike" or command == "Dislike":
        st.write(negative_fb)
def convert_image_format(image, new_format):
    try:
        img = Image.open(image)
        img = img.convert('RGB')
        img.save(f'converted_image.{new_format}', format=new_format)
        return True, f'converted_image.{new_format}'
    except Exception as e:
        return False, str(e)
        
def edit_img():
    st.write("🤓 Images processing tool 🤓")
    term_rgb = st.text_input("Please enter RGB values (e.g., '0,2,1'):")
    try:
        term_rgb = term_rgb.strip().split(',')
        if len(term_rgb) != 3:
            st.error("Please enter exactly three RGB values separated by commas.")
            return
        t_r, t_g, t_b = [int(cr) for cr in term_rgb]

    except ValueError:
        st.error("Invalid input. Please enter numeric values.")
    uploaded_file = st.file_uploader("Upload your file.", type=['png', 'jpeg', 'jpg'])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img)
        st.image(change_img(img, t_r, t_g, t_b))
        
    uploaded_file = st.file_uploader("Choose an image to tranform its form.", type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Image', use_column_width=True)

        new_format = st.selectbox('Select the new format:', ['JPEG', 'PNG', 'ICO'])
        if st.button('Convert'):
            format_ext = new_format.lower()
            success, message = convert_image_format(uploaded_file, format_ext)
            if success:
                with open(f"./converted_image.{format_ext}", 'rb') as f:
                    temp_pic = f.read()
                    dl_fr = st.download_button(label="Download images", data=temp_pic, file_name=f'converted_img.{format_ext}')
            else:
                st.error(f'Error: {message}')

def change_img(img, rc, gc, bc):
    width, height = img.size
    img_array = img.load()
    try:
        for x in range(width):
            for y in range(height):
                r = img_array[x, y][int(rc)]
                g = img_array[x, y][int(gc)]
                b = img_array[x, y][int(bc)]
                img_array[x, y] = (r,g,b)
        return img
    except:
        img_error = ":red[Error processing image. Please check your input.]"
        st.write(img_error)
        
def google_trans(text, target):
    if text != '' and target != '':
        url = "https://findmyip.net/api/translate.php"
        params = {
            "text": text,
            "target_lang": target
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                try:
                    data = response.json()
                    translate_result = data["data"]["translate_result"]
                    st.markdown("### Translation result:")
                    st.write(translate_result)
                except:
                    st.error("Unvalid inputs.")
            else:
                st.error(f"Failed to request: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")

        
def smart_dict_page():
    st.markdown("## 📚 My Smart Dictionary 📚")
    st.markdown("### Local dictionary")
    with open('words_space.txt', 'r', encoding='utf-8') as f:
        words_list = f.read().split("\n")
    for i in range(len(words_list)):
        words_list[i] = words_list[i].split('#')
    words_dict = {}
    for i in words_list:
        words_dict[i[1]] = [int(i[0]), i[2]]
    with open('check_out_times.txt', 'r', encoding='utf-8') as f:
        times_list = f.read().split('\n')
    for i in range(len(times_list)):
        times_list[i] = times_list[i].split('#')
    times_dict = {}
    for i in times_list:
        times_dict[int(i[0])] = int(i[1])
        
    word = st.text_input('Please write the word you want to query.')
    if word in words_dict:
        st.write(words_dict[word])
        n = words_dict[word][0]
        if n in times_dict:
            times_dict[n] += 1
        else:
            times_dict[n] = 1
            
        st.write('query times:', times_dict[n])
        if word == 'balloon':
            st.balloons()
    elif word == '':
        pass
    else:
        error_query_dic = ":red[Fail to query. May be the word is un-dictionaried.]"
        st.write(error_query_dic)
    st.markdown("### The words are un-dictionaried? Try google translator↓")
    google_text = st.text_input("Please type the word you want to query below.")
    google_target = st.text_input("Please type the short form of the target language you want to query below.")
    google_trans(google_text, google_target)
    st.markdown("[A Comprehensive List of Abbreviations for World Languages](https://blog.csdn.net/zixiao217/article/details/118251174)")

def discussion_area_page():
    st.write("💬 My Discussion Area 💬")
    with open('leave_messages.txt', 'r', encoding='utf-8') as f:
        message_list = [line.split('#') for line in f.read().split('\n') if line.strip()]
    if not message_list or not message_list[-1][0].isdigit():
        newd = 1
    else:
        newd = int(message_list[-1][0]) + 1
    for i in message_list:
        if len(i) >= 3:
            if i[1] == 'Jack':
                with st.chat_message('👓'):
                    st.write(i[1], ':', i[2])
            elif i[1] == 'Kitten':
                with st.chat_message('🐱'):
                    st.write(i[1], ':', i[2])
            else:
                with st.chat_message('🙂'):
                    st.write(i[1], ':', i[2])

    username = input("请输入你的用户名（登录系统出现问题，暂时用该方法代替）")
    st.write(f"You are logged in as: {username}")
    new_message = st.chat_input("Let's chat!")
    if new_message and new_message != '':
        message_list.append([str(newd), username, new_message])
        with open('leave_messages.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(['#'.join(msg) for msg in message_list]))
        st.rerun()

def spark_ai(chat):
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    data = {
            "model": "general",
            "messages": [
                {
                    "role": 'user',
                    "content": chat
                }
            ],
               "stream": False
        }
    header = {
        "Authorization": "Bearer 1c427588380d4d2f20d5efd75e9a52a0:ZmRhMTM4MDBmZWRmMjE3YWE2ODEyNDZm"
    }
    st.markdown("#### AI")
    with st.spinner("AI is thinking..."):
        response = requests.post(url, headers=header, json=data)
        response.encoding = "utf-8"
        try:
            response_data = response.json()
            content = response_data['choices'][0]['message']['content']
            st.markdown(content)
        except:
            st.error("Error! Try again after a while.")
        # except (json.JSONDecodeError, KeyError) as e:
        #     st.error(f"Error parsing response: {e}")
        #     response_data = response.json()
        #     st.markdown(response_data['choices'][0])


def about_page():
    st.write("## Spark Model AI(NOT support context)")
    speak_info = st.chat_input("Let's chat!")
    st.write("AI can make mistakes. Check import Info. \n If there is a TimeoutError, please try again after a while.")
    if speak_info:
        ask1, ask2 = st.columns([1.5,1])
        with ask2:
            st.markdown('''
                        ```
                        '''+speak_info)
        spark_ai(speak_info)

page = st.sidebar.radio("My Page", ['Favorites Recommendation', 'My images processing tools', 'My Smart Dictionary', 'My Discussion Area', 'Spark Lite AI'])
if page == 'Favorites Recommendation':
    fr_page()
elif page == 'My images processing tools':
    edit_img()
elif page == 'My Smart Dictionary':
    smart_dict_page()
elif page == 'My Discussion Area':
    discussion_area_page()
elif page == 'Spark Lite AI':
    about_page()
