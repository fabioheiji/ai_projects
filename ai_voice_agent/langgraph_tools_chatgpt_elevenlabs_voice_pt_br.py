from typing import TypedDict, Optional
import speech_recognition as sr
import re
import os
from langgraph.graph import StateGraph, END
from langchain_community.tools import DuckDuckGoSearchResults
import whisper
import warnings
import openai
from openai import Client
from elevenlabs import play  # Corrected import for ElevenLabs usage :contentReference[oaicite:0]{index=0}
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings('ignore')

# Set your OpenAI and Eleven Labs API keys in the .env file

# --- Agente de Reconhecimento de Fala para Texto ---
class SpeechToTextAgent:
    def __init__(self):
        self.sample_rate: int = 16000
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=0, sample_rate=self.sample_rate)
        
    def capture_audio(self) -> sr.AudioData:
        print("\nOuvindo...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.recognizer.pause_threshold = 2.0  # segundos de silêncio para considerar o fim de uma frase
            audio = self.recognizer.listen(source)
        return audio

    def save_audio_data(self, audio: sr.AudioData, filename: str, sample_rate: int = 16000) -> None:
        """
        Salva os dados de áudio (AudioData do SpeechRecognition) em um arquivo WAV.
        
        Parâmetros:
            audio (sr.AudioData): Os dados de áudio gravados.
            filename (str): Caminho para salvar o arquivo WAV.
            sample_rate (int): A taxa de amostragem para conversão.
        """
        wav_bytes = audio.get_wav_data(convert_rate=sample_rate)
        with open(filename, "wb") as f:
            f.write(wav_bytes)
        # print(f"Áudio salvo em {filename}")

    def convert_to_text(self, audio: sr.AudioData) -> str:
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Não foi possível entender o áudio"
        except sr.RequestError:
            return "API indisponível"

    def transcribe_with_whisper(self, filename: str, language: str = "pt", model_size: str = "medium") -> str:
        """
        Transcreve o arquivo de áudio usando o Whisper.
        
        Parâmetros:
            filename (str): Caminho para o arquivo WAV.
            language (str): Código do idioma para forçar a transcrição (ex.: "pt" para Português).
            model_size (str): Tamanho do modelo Whisper (ex.: "tiny", "base", "small", "medium", "large").
        
        Retorna:
            str: O texto transcrito.
        """
        model = whisper.load_model(model_size)
        result = model.transcribe(filename, language=language)
        return result["text"]

# --- Agente de Texto para Fala ---
class TextToSpeechAgent:
    def __init__(self):
        self.language = 'pt-br'
        
    def convert_to_speech(self, text: str):
        client = ElevenLabs()
        audio = client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )        
        # audio = generate(
        #     text=text,
        #     voice="Bella",  # Escolha uma voz da ElevenLabs
        #     model="eleven_multilingual_v1"
        # )
        play(audio)

# --- Utiliza a ferramenta DuckDuckGo pré-definida ---
duckduckgo_tool = DuckDuckGoSearchResults()

# --- Define a estrutura de estado ---
class AgentState(TypedDict):
    user_input: str
    messages: list[dict]
    tool_required: bool
    tool_query: Optional[str]
    tool_result: Optional[str]
    final_response: Optional[str]

# --- Inicializa os Agentes ---
stt_agent = SpeechToTextAgent()
tts_agent = TextToSpeechAgent()

# --- Prompt do Sistema ---
SYSTEM_PROMPT = """Você é um assistente útil com acesso a ferramentas.
Quando precisar pesquisar informações atuais, utilize o formato:
<SEARCH>consulta de pesquisa aqui</SEARCH>

Sempre forneça sua resposta final após o uso de qualquer ferramenta.
Responda sempre em Português do Brasil."""

def parse_tool_calls(response: str) -> dict:
    """Analisa a resposta do modelo para detectar chamadas de ferramenta"""
    search_match = re.search(r'<SEARCH>(.*?)</SEARCH>', response)
    if search_match:
        return {
            'tool_required': True,
            'tool_name': 'duckduckgo_search',
            'tool_query': search_match.group(1).strip()
        }
    return {'tool_required': False}

# --- Define as Funções dos Nós ---
def speech_to_text_node(state: AgentState):
    audio = stt_agent.capture_audio()
    stt_agent.save_audio_data(audio, "user_input.wav")
    user_input = stt_agent.transcribe_with_whisper("user_input.wav")
    # Alternativamente, pode usar:
    # user_input = stt_agent.convert_to_text(audio)
    print(f"\nUsuário: {user_input}")
    return {
        "user_input": user_input,
        "messages": [{"role": "user", "content": user_input}]
    }

def generate_response_node(state: AgentState):
    messages = state["messages"]
    
    # Adiciona o prompt do sistema se for a primeira mensagem
    if not any(msg["role"] == "system" for msg in messages):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    
    # Se houver resultados da pesquisa, inclui-os no contexto
    if state.get("tool_result"):
        messages.append({
            "role": "system",
            "content": f"Resultados da pesquisa: {state['tool_result']}\nAgora forneça sua resposta final:"
        })
    
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=messages,
        temperature=0
    )

    content = response.choices[0].message.content
    tool_data = parse_tool_calls(content)
    
    if tool_data['tool_required']:
        print(f"Requisição de ferramenta detectada: {tool_data['tool_query']}")
        return {
            "tool_required": True,
            "tool_query": tool_data['tool_query'],
            "messages": messages + [{"role": "assistant", "content": content}]
        }
    
    print(f'generate_response_node | messages: {messages}')
    
    return {
        "tool_required": False,
        "final_response": content,
        "messages": messages + [{"role": "assistant", "content": content}]
    }

def search_tool_node(state: AgentState):
    result = duckduckgo_tool.invoke({"query": state["tool_query"]})
    print(f"Resultados da pesquisa: {result[:200]}...")  # Trunca para exibição
    return {"tool_result": result}

def text_to_speech_node(state: AgentState):
    if state.get("final_response"):
        print(f"\nAssistente: {state['final_response']}")
        tts_agent.convert_to_speech(state["final_response"])
    return state

# --- Monta o Workflow com LangGraph ---
workflow = StateGraph(AgentState)

workflow.add_node("speech_to_text", speech_to_text_node)
workflow.add_node("generate_response", generate_response_node)
workflow.add_node("search_tool", search_tool_node)
workflow.add_node("text_to_speech", text_to_speech_node)

workflow.set_entry_point("speech_to_text")
workflow.add_edge("speech_to_text", "generate_response")

def route_after_generation(state: AgentState):
    if state.get("tool_required"):
        return "search_tool"
    return "text_to_speech"

workflow.add_conditional_edges(
    "generate_response",
    route_after_generation,
    {
        "search_tool": "search_tool",
        "text_to_speech": "text_to_speech"
    }
)

workflow.add_edge("search_tool", "generate_response")
workflow.add_edge("text_to_speech", "speech_to_text")

app = workflow.compile()

def main():
    try:
        app.invoke({
            "user_input": "",
            "messages": [],
            "tool_required": False
        })
    except KeyboardInterrupt:
        print("\nSaindo...")

if __name__ == "__main__":
    main()
