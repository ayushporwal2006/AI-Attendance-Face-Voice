from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st 

@st.cache_resource
def voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    try:
        encoder = VoiceEncoder()

        audio , sr = librosa.load(io.bytesIO(audio_bytes), sr =16000) # more sample rate(sr) means more clear sound 
        wav = preprocess_wav(audio) # Normalise the audio by removal of noise
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()  # creates 256 dimension vector
    except Exception as e:
        st.error("Voice recognition error")
        return None

def identify_speaker(new_embedding, candidate_dict, threshold =0.65):
    if not new_embedding or not candidate_dict:
        return None, 0.0
    
    best_sid = None  # sid = student id
    best_score = -1.0

    for sid, stored_embedding in candidate_dict:
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding) # vectors jitne jyada close honge utni similarity hogi
            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score <= threshold:
        return best_sid, best_score
    
    return None, best_score

def process_bulk_audio(audio_bytes,candidate_dict,threshold =0.65):
     try:
        encoder = VoiceEncoder()

        audio , sr = librosa.load(io.bytesIO(audio_bytes), sr =16000) # more sample rate(sr) means more clear sound 
        segment = librosa.effects.split(audio , top_db=30)# to provide long audio into segment and skip where no voice or less voice
                                                # top_db = sensitity of voice 
        identified_result = {}

        for start, end in segment:
            if (start-end)< sr * 0.5: # remove garbage sound or less voice
                continue
            segment_audio = audio[start: end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(embedding,candidate_dict,threshold)

            if sid:
                if sid not in identify_speaker or score> identified_result[sid]:
                    identified_result[sid] = score

        return identified_result
     except Exception as e:
         st.error("Bulk process error")
         return {}



                

