
import streamlit as st
import webuiapi
import uuid
from rembg import new_session, remove

def main():
    st.set_page_config(
        page_title="Create SimCity Style Buildings With Stable Diffusion",
        page_icon="😺")
    
    # create API client
    #api = webuiapi.WebUIApi()
    api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)
    #api = webuiapi.WebUIApi(host='webui.example.com', port=443, use_https=True)
    
    #Set the model to be used by stable diffusion
    options = {}
    options['sd_model_checkpoint'] = "gameIconInstitute_v30.safetensors [c112297163]"
    api.set_options(options)

    #Set the model to be used for removing the background of the image
    session = new_session("u2net")

    container = st.container()
    with container:
        with st.form(key="my form", clear_on_submit=True):
            user_input  = st.text_area(label="Building Description: ", key="input", height = 100)
            submit_button = st.form_submit_button(label="Create!")

        if submit_button:

            if not user_input:
                user_input = 'magic zoo'
                
            with st.spinner("Thinking..."):
                st.write(f"Building Description: {user_input}")

                #Build the prompt
                prompt = "Isometric_Setting,building exterior,(black background),<lora:Stylized_ Setting SDXL:4>,"
                prompt += user_input

                #create the character picture
                result = api.txt2img(prompt=prompt,
                    negative_prompt="out of frame,cut off",
                    cfg_scale=7,
                    width=768,
                    height=512,
                    steps=40,
                    save_images=True)
                
                #save the image to the sdresults folder
                filename = f"{uuid.uuid4()}.png"
                sdfilename = f"sdresults/{filename}"
                result.image.save(sdfilename, "PNG")

                #remove the background
                output_image = remove(result.image, session=session)

                #save the image to the nobackground folder
                nbfilename = f"nobackground/{filename}"
                output_image.save(nbfilename, "PNG")

                #display the image in StreamLit
                st.image(nbfilename)

if __name__ == "__main__":
    main()