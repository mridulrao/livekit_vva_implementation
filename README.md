This is boiler plate / quickstart implementation of Livekit VVA 

Currently it uses Livekit SIP and Twilio as SIP Trunk Provider. Other SIP Trunk provider like Azure Commmunicaiton Service and Genesys needs to looked into. 

Two implementation 
1) S2S Model - Uses openAI real time API 
2) TTS Model - Uses STT/TTS/LLM based voice pipeline 


Demo 
1) Install dependencies
 - https://github.com/livekit/python-sdks

3) Update the env with credentials 

4) Navigate to tts_model folder and run 'python main.py dev'

5) Call the phone number +1 650 870 9225 
 - Use 9080 as verification - its harcoded right now 
 - Discuss the issue like 'My system is running really slow'

